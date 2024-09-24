from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings
from django.db import transaction
import logging
from django_rq import job  # Redis Queue를 사용한 비동기 처리를 위해

logger = logging.getLogger(__name__)

@job  # Redis Queue를 통해 비동기로 작업을 처리하기 위한 데코레이터
def sync_to_other_db(sender, instance_user_id, created, **kwargs):
    model = apps.get_model(app_label=sender._meta.app_label, model_name=sender._meta.model_name)
    other_db = 'local_db' if settings.DATABASES['default'] == settings.DATABASES['heroku_db'] else 'heroku_db'
    source_db = 'heroku_db' if other_db == 'local_db' else 'default'
    
    logger.info(f"사용자 ID {instance_user_id}를 {settings.DATABASES['default']}에서 {other_db}로 동기화 시도 중")
    
    try:
        with transaction.atomic(using=other_db):
            # 여기서 'default' 대신 source_db 사용
            instance = model.objects.using(source_db).get(user_id=instance_user_id)
            logger.info(f"원본 데이터베이스에서 사용자를 찾았습니다: {instance}")
            
            other_instance, created = model.objects.using(other_db).get_or_create(user_id=instance.user_id)
            if created:
                logger.info(f"대상 데이터베이스에 새 사용자를 생성: {other_instance}")
            else:
                logger.info(f"대상 데이터베이스의 기존 사용자를 업데이트 중: {other_instance}")
            
            for field in instance._meta.fields:
                if field.name != 'user_id':  # 기본 키는 업데이트하지 않음
                    setattr(other_instance, field.name, getattr(instance, field.name))
            other_instance.save(using=other_db)
            logger.info(f"대상 데이터베이스에서 사용자를 업데이트: {other_instance}")
        
        logger.info(f"사용자 ID {instance_user_id}를 {other_db}로 동기화 성공")
    except model.DoesNotExist:
        logger.warning(f"원본 데이터베이스에서 사용자 ID {instance_user_id}를 찾을 수 없습니다. 건너뛰기")
    except Exception as e:
        logger.error(f"사용자 ID {instance_user_id}를 {other_db}로 동기화하는 데 실패했습니다: {str(e)}", exc_info=True)


@job  # 삭제 동작도 비동기로 처리
def sync_delete_to_other_db(sender, instance_user_id, **kwargs):
    # 데이터베이스 라우터가 설정되지 않았다면 동기화 작업을 하지 않음
    if not settings.DATABASE_ROUTERS:
        return
    
    # 동기화 대상 데이터베이스 설정 ('local_db'에서 'heroku_db'로 또는 그 반대)
    other_db = 'heroku_db' if settings.DATABASES['default'] == settings.DATABASES['local_db'] else 'local_db'
    source_db = 'heroku_db' if other_db == 'local_db' else 'default'
    
    model = apps.get_model(app_label=sender._meta.app_label, model_name=sender._meta.model_name)
    
    try:
        with transaction.atomic(using=other_db):
            model.objects.using(other_db).filter(user_id=instance_user_id).delete()
        logger.info(f"{source_db}에서 삭제된 ID가 {instance_user_id}인 {model.__name__}를 {other_db}에서도 성공적으로 삭제했습니다")
    except Exception as e:
        logger.error(f"{other_db}에서 ID가 {instance_user_id}인 {model.__name__} 삭제 실패: {str(e)}")

# 모델 저장 및 삭제 시 시그널을 연결하는 함수
def register_sync_signals():
    for model in apps.get_models():
        # 모델 저장 시 sync_to_other_db 작업을 비동기로 큐에 추가
        post_save.connect(lambda sender, instance, created, **kwargs: sync_to_other_db.delay(sender, instance.user_id, created, **kwargs), sender=model)
        # 모델 삭제 시 sync_delete_to_other_db 작업을 비동기로 큐에 추가
        post_delete.connect(lambda sender, instance, **kwargs: sync_delete_to_other_db.delay(sender, instance.user_id, **kwargs), sender=model)