import os

class DatabaseRouter:
    def db_for_read(self, model, **hints):
        return self._get_db()

    def db_for_write(self, model, **hints):
        return self._get_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

    def allow_syncdb(self, db, model):
        return True

    def _get_db(self):
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'harvy_portfolio.settings_prod':
            return 'default'  # Heroku 환경
        else:
            return 'default'  # 로컬 환경

    def get_other_db(self):
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'harvy_portfolio.settings_prod':
            return 'local_db'  # Heroku 환경에서 동기화 대상 DB
        else:
            return 'heroku_db'  # 로컬 환경에서 동기화 대상 DB