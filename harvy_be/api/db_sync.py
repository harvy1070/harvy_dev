from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings
from django.db import transaction
import logging
from django_rq import job  # Redis Queue를 사용한 비동기 처리를 위해

logger = logging.getLogger(__name__)

@job  # Redis Queue를 통해 비동기로 작업을 처리하기 위한 데코레이터
def sync_to_other_db(sender, instance_id, created, **kwargs):
    # 데이터베이스 라우터가 설정되지 않았다면 동기화 작업을 하지 않음
    if not settings.DATABASE_ROUTERS:
        return
    
    # 동기화 대상 데이터베이스를 설정 ('local_db'에서 'heroku_db'로, 또는 그 반대)
    other_db = 'heroku_db' if settings.DATABASES['default'] == settings.DATABASES['local_db'] else 'local_db'
    
    # 시그널을 보낸 모델의 정보를 가져옴
    model = apps.get_model(app_label=sender._meta.app_label, model_name=sender._meta.model_name)
    
    try:
        # 트랜잭션을 사용하여 동기화 대상 데이터베이스에서 작업을 수행 (동기화가 완료될 때까지 롤백 방지)
        with transaction.atomic(using=other_db):
            # 기본 데이터베이스에서 인스턴스를 가져옴
            instance = model.objects.using('default').get(pk=instance_id)
            if created:
                # 새로운 인스턴스를 동기화 대상 데이터베이스에 생성
                model.objects.using(other_db).create(**{f.name: getattr(instance, f.name) for f in instance._meta.fields})
            else:
                # 수정된 인스턴스를 동기화 대상 데이터베이스에서 가져와 업데이트
                other_instance, created = model.objects.using(other_db).get_or_create(pk=instance.pk)
                for field in instance._meta.fields:
                    setattr(other_instance, field.name, getattr(instance, field.name))
                other_instance.save(using=other_db)
        logger.info(f"Successfully synced {model.__name__} with id {instance_id} to {other_db}")
    except Exception as e:
        # 오류 발생 시 로그를 기록
        logger.error(f"Failed to sync {model.__name__} with id {instance_id} to {other_db}: {str(e)}")

@job  # 삭제 동작도 비동기로 처리
def sync_delete_to_other_db(sender, instance_id, **kwargs):
    # 데이터베이스 라우터가 설정되지 않았다면 동기화 작업을 하지 않음
    if not settings.DATABASE_ROUTERS:
        return
    
    # 동기화 대상 데이터베이스 설정 ('local_db'에서 'heroku_db'로 또는 그 반대)
    other_db = 'heroku_db' if settings.DATABASES['default'] == settings.DATABASES['local_db'] else 'local_db'
    
    # 시그널을 보낸 모델의 정보를 가져옴
    model = apps.get_model(app_label=sender._meta.app_label, model_name=sender._meta.model_name)
    
    try:
        # 트랜잭션을 사용하여 삭제 작업을 처리
        with transaction.atomic(using=other_db):
            # 다른 데이터베이스에서 동일한 객체를 삭제
            model.objects.using(other_db).filter(pk=instance_id).delete()
        logger.info(f"Successfully deleted {model.__name__} with id {instance_id} from {other_db}")
    except Exception as e:
        # 오류 발생 시 로그를 기록
        logger.error(f"Failed to delete {model.__name__} with id {instance_id} from {other_db}: {str(e)}")

# 모델 저장 및 삭제 시 시그널을 연결하는 함수
def register_sync_signals():
    for model in apps.get_models():
        # 모델 저장 시 sync_to_other_db 작업을 비동기로 큐에 추가
        post_save.connect(lambda sender, instance, created, **kwargs: sync_to_other_db.delay(sender, instance.id, created, **kwargs), sender=model)
        # 모델 삭제 시 sync_delete_to_other_db 작업을 비동기로 큐에 추가
        post_delete.connect(lambda sender, instance, **kwargs: sync_delete_to_other_db.delay(sender, instance.id, **kwargs), sender=model)