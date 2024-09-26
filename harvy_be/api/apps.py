from django.apps import AppConfig
import logging
import sys

logger = logging.getLogger(__name__)

# db_sync를 위한 수정 / 9.23.
class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from .db_sync import register_sync_signals
        register_sync_signals()
        logger.error("싱크 로그 확인용 (error로그 출력되어야함)")