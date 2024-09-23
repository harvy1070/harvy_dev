from django.apps import AppConfig

# db_sync를 위한 수정 / 9.23.
class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from .db_sync import register_sync_signals
        register_sync_signals()