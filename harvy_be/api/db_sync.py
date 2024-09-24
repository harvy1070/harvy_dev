from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings
from django.db import transaction
import logging
from django_rq import job

logger = logging.getLogger(__name__)

@job
def sync_to_other_db(sender, instance_pk, created, **kwargs):
    model = sender
    
    # 현재 데이터베이스와 대상 데이터베이스 결정
    current_db = 'default'
    other_db = 'heroku_db' if current_db == 'default' else 'default'
    
    logger.info(f"{model.__name__} ID {instance_pk}를 {current_db}에서 {other_db}로 동기화 시도 중")
    
    try:
        with transaction.atomic(using=other_db):
            # 현재 DB에서 인스턴스 가져오기
            instance = model.objects.using(current_db).get(pk=instance_pk)
            logger.info(f"현재 DB({current_db})에서 {model.__name__}를 찾았습니다: {instance}")
            
            # 필요한 필드만 딕셔너리로 추출
            instance_data = {f.name: getattr(instance, f.name) for f in instance._meta.fields if f.name != 'id'}
            
            # 대상 DB에서 업데이트 또는 생성
            other_instance, created = model.objects.using(other_db).update_or_create(
                pk=instance_pk,
                defaults=instance_data
            )
            
            if created:
                logger.info(f"대상 DB({other_db})에 새 {model.__name__}를 생성: {other_instance}")
            else:
                logger.info(f"대상 DB({other_db})의 기존 {model.__name__}를 업데이트: {other_instance}")
        
        logger.info(f"{model.__name__} ID {instance_pk}를 {other_db}로 동기화 성공")
    except model.DoesNotExist:
        logger.warning(f"현재 DB({current_db})에서 {model.__name__} ID {instance_pk}를 찾을 수 없습니다. 건너뛰기")
    except Exception as e:
        logger.error(f"{model.__name__} ID {instance_pk}를 {other_db}로 동기화하는 데 실패했습니다: {str(e)}", exc_info=True)

@job
def sync_delete_to_other_db(sender, instance_pk, **kwargs):
    model = sender
    current_db = 'default'
    other_db = 'heroku_db' if current_db == 'default' else 'default'
    
    logger.info(f"{model.__name__} ID {instance_pk}를 {other_db}에서 삭제 시도 중")
    
    try:
        with transaction.atomic(using=other_db):
            model.objects.using(other_db).filter(pk=instance_pk).delete()
        logger.info(f"{other_db}에서 {model.__name__} ID {instance_pk} 삭제 성공")
    except Exception as e:
        logger.error(f"{other_db}에서 {model.__name__} ID {instance_pk} 삭제 실패: {str(e)}")

def register_sync_signals():
    logger.info("Registering sync signals...")
    from .models import UserInfo, QnA, PortfolioBoard, PortfolioFiles, PjTimeline
    
    models_to_sync = [UserInfo, QnA, PortfolioBoard, PortfolioFiles, PjTimeline]
    
    def sync_handler(sender, instance, created, **kwargs):
        logger.info(f"Sync handler called for {sender.__name__} with pk {instance.pk}")
        transaction.on_commit(lambda: sync_to_other_db.delay(sender, instance.pk, created, **kwargs))

    for model in models_to_sync:
        post_save.connect(sync_handler, sender=model)
        post_delete.connect(lambda sender, instance, **kwargs: sync_delete_to_other_db.delay(sender, instance.pk, **kwargs), sender=model)
    
    logger.info("Sync signals registered successfully")