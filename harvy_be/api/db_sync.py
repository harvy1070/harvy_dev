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
    
    # 현재 데이터베이스와 대상 데이터베이스 결정
    current_db = 'default'
    other_db = 'heroku_db' if current_db == 'default' else 'default'
    
    logger.info(f"사용자 ID {instance_user_id}를 {current_db}에서 {other_db}로 동기화 시도 중")
    
    try:
        with transaction.atomic(using=other_db):
            # 현재 DB에서 인스턴스 가져오기
            instance = model.objects.using(current_db).get(user_id=instance_user_id)
            logger.info(f"현재 DB({current_db})에서 사용자를 찾았습니다: {instance}")
            
            # 필요한 필드만 딕셔너리로 추출
            instance_data = {f.name: getattr(instance, f.name) for f in instance._meta.fields if f.name != 'id'}
            
            # 대상 DB에서 업데이트 또는 생성
            other_instance, created = model.objects.using(other_db).update_or_create(
                user_id=instance_user_id,
                defaults=instance_data
            )
            
            if created:
                logger.info(f"대상 DB({other_db})에 새 사용자를 생성: {other_instance}")
            else:
                logger.info(f"대상 DB({other_db})의 기존 사용자를 업데이트: {other_instance}")
        
        logger.info(f"사용자 ID {instance_user_id}를 {other_db}로 동기화 성공")
    except model.DoesNotExist:
        logger.warning(f"현재 DB({current_db})에서 사용자 ID {instance_user_id}를 찾을 수 없습니다. 건너뛰기")
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
    from .models import UserInfo  # UserInfo 모델을 import
    
    def sync_handler(sender, instance, created, **kwargs):
        transaction.on_commit(lambda: sync_to_other_db.delay(sender, instance.user_id, created, **kwargs))

    post_save.connect(sync_handler, sender=UserInfo)
    post_delete.connect(lambda sender, instance, **kwargs: sync_delete_to_other_db.delay(sender, instance.user_id, **kwargs), sender=UserInfo)