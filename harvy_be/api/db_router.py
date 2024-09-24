# db router 구현(db_sync 작업용)
class DatabaseRouter:
    def db_for_read(self, model, **hints):
        # 읽기 작업은 기본적으로 'default' DB를 사용
        return 'default'

    def db_for_write(self, model, **hints):
        # 쓰기 작업도 기본적으로 'default' DB를 사용
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # 모든 DB 간의 관계를 허용
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # 모든 DB에 대해 마이그레이션을 허용
        return True

    def allow_syncdb(self, db, model):
        # 모든 모델의 동기화를 허용
        return True