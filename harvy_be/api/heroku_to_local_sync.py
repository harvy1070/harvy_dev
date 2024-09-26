# 수동으로 Heroku DB -> Local DB(DBeaver, Postgre)로 동기화
# python c:\harvy_dev\harvy_be\api\heroku_to_local_sync.py 실행

import os, sys
import django
import psycopg2
from django.db import connections
from django.conf import settings

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Django 설정 로드 (개발 환경 설정 사용)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "harvy_portfolio.settings_dev")
django.setup()

def is_local_db_active():
    try:
        connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        connection.close()
        return True
    except psycopg2.OperationalError:
        return False

def sync_data():
    if not is_local_db_active():
        print("로컬 데이터베이스가 활성화되지 않았습니다. 동기화를 건너뜁니다.")
        return

    models_to_sync = ['UserInfo', 'QnA', 'PortfolioBoard', 'PortfolioFiles', 'PjTimeline']

    for model_name in models_to_sync:
        model = django.apps.apps.get_model(app_label='api', model_name=model_name)
        
        # Heroku DB에서 데이터 가져오기
        heroku_objects = model.objects.using('heroku_db').all()
        
        for obj in heroku_objects:
            # 로컬 DB에 데이터 동기화
            model.objects.using('default').update_or_create(
                pk=obj.pk,
                defaults={field.name: getattr(obj, field.name) for field in obj._meta.fields if field.name != 'id'}
            )
        
        print(f"{model_name} 모델 동기화 완료")

if __name__ == "__main__":
    sync_data()