# 현재는 여건상 실시간 비동기 작업을 실행하지 않으려고 함
# - 실시간으로 진행 시 추가적인 요금에 대해 감당할 수 없을 것 같음..

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings
from django.db import transaction
import logging
from django_rq import job
from api.db_router import DatabaseRouter

logger = logging.getLogger('api')

# sync_to_other_db 작업 내역
# 한 데이터베이스의 변경사항을 다른 데이터베이스에 동기화하는 함수
# 1. 모델과 데이터베이스 정보 가져오기
# 2. 트랜잭션 내에서 다른 DB에 데이터 update_or_create
# 3. 로깅 수행
@job
def sync_to_other_db(model_name, instance_pk, created, **kwargs):
    logger.info(f"{model_name} 모델의 ID {instance_pk}에 대한 동기화 작업이 시작되었습니다.")
    model = apps.get_model(app_label='api', model_name=model_name)
    
    router = DatabaseRouter()
    current_db = router._get_db()
    other_db = router.get_other_db()
    
    logger.info(f"{model_name} ID {instance_pk}을(를) {current_db}에서 {other_db}로 동기화 시도 중")
    
    try:
        with transaction.atomic(using=other_db):
            instance = model.objects.using(current_db).get(pk=instance_pk)
            instance_data = {f.name: getattr(instance, f.name) for f in instance._meta.fields if f.name != 'id'}
            
            other_instance, created = model.objects.using(other_db).update_or_create(
                pk=instance_pk,
                defaults=instance_data
            )
            
            if created:
                logger.info(f"{other_db} 데이터베이스에 새 {model_name} 객체가 생성되었습니다: {other_instance}")
            else:
                logger.info(f"{other_db} 데이터베이스에 기존 {model_name} 객체가 업데이트되었습니다: {other_instance}")
        
        logger.info(f"{model_name} ID {instance_pk}가 {other_db}로 성공적으로 동기화되었습니다.")
    except model.DoesNotExist:
        logger.warning(f"{current_db} 데이터베이스에서 {model_name} ID {instance_pk} 객체를 찾을 수 없습니다. 작업을 건너뜁니다.")
    except Exception as e:
        logger.error(f"{model_name} ID {instance_pk} 객체를 {other_db}로 동기화하는 데 실패했습니다: {str(e)}", exc_info=True)

# sync_delete_to_other_db 작업 내역  
# 한 데이터베이스의 삭제 작업을 다른 데이터베이스에 동기화하는 함수
# 1. 모델과 데이터베이스 정보 가져오기
# 2. 트랜잭션 내에서 다른 DB에서 해당 객체 삭제
# 3. 로깅 수행
@job
def sync_delete_to_other_db(model_name, instance_pk, **kwargs):
    model = apps.get_model(app_label='api', model_name=model_name)
    
    router = DatabaseRouter()
    current_db = router._get_db()
    other_db = router.get_other_db()
    
    logger.info(f"{model_name} ID {instance_pk} 객체를 {other_db}에서 삭제 시도 중")
    
    try:
        with transaction.atomic(using=other_db):
            model.objects.using(other_db).filter(pk=instance_pk).delete()
        logger.info(f"{other_db} 데이터베이스에서 {model_name} ID {instance_pk} 객체가 성공적으로 삭제되었습니다.")
    except Exception as e:
        logger.error(f"{other_db} 데이터베이스에서 {model_name} ID {instance_pk} 객체를 삭제하는 데 실패했습니다: {str(e)}")

# register_sync_signal 작업 내역
# 동기화를 위한 신호(signal)를 등록하는 함수
# 1. 동기화할 모델 목록 정의
# 2. 각 모델에 대해 post_save와 post_delete 신호 연결
# 3. 신호 핸들러 함수 정의 (sync_handler, delete_handler)
def register_sync_signals():
    logger.info("동기화 신호를 등록하는 중...")
    from .models import UserInfo, QnA, PortfolioBoard, PortfolioFiles, PjTimeline
    
    models_to_sync = [UserInfo, QnA, PortfolioBoard, PortfolioFiles, PjTimeline]
    
    def sync_handler(sender, instance, created, **kwargs):
        logger.debug(f"{sender.__name__} 모델의 ID {instance.pk}에 대한 동기화 핸들러가 호출되었습니다.")
        try:
            job = sync_to_other_db.delay(sender.__name__, instance.pk, created)
            logger.debug(f"작업이 큐에 추가되었습니다. 작업 ID: {job.id}")
        except Exception as e:
            logger.error(f"작업을 큐에 추가하는 데 실패했습니다: {str(e)}", exc_info=True)
    
    def delete_handler(sender, instance, **kwargs):
        transaction.on_commit(lambda: sync_delete_to_other_db.delay(sender.__name__, instance.pk))

    for model in models_to_sync:
        logger.error(f"모델명 {model.__name__}에 대한 신호 연결 중")
        post_save.connect(sync_handler, sender=model)
        post_delete.connect(delete_handler, sender=model)
    
    logger.error("동기화 신호가 성공적으로 등록되었습니다.")
