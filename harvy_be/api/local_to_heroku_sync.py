import os
import sys
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

# 로컬 데이터베이스 연결을 확인하는 함수
# 연결이 성공하면 True, 실패하면 False를 반환
def is_heroku_db_active():
    try:
        connection = psycopg2.connect(
            dbname=settings.DATABASES['heroku_db']['NAME'],
            user=settings.DATABASES['heroku_db']['USER'],
            password=settings.DATABASES['heroku_db']['PASSWORD'],
            host=settings.DATABASES['heroku_db']['HOST'],
            port=settings.DATABASES['heroku_db']['PORT'],
        )
        connection.close()
        return True
    except psycopg2.OperationalError:
        return False

# Heroku DB에서 로컬 DB로 데이터를 동기화하는 주요 함수
# 1. 로컬 DB 활성화 여부 확인
# 2. 동기화할 모델 목록 정의
# 3. 각 모델에 대해:
#    - Heroku DB에서 데이터 가져오기
#    - 로컬 DB에 데이터 update_or_create
def sync_data():
    if not is_heroku_db_active():
        print("Heroku 데이터베이스에 연결할 수 없습니다. 동기화를 건너뜁니다.")
        return

    models_to_sync = ['UserInfo', 'QnA', 'PortfolioBoard', 'PortfolioFiles', 'PjTimeline']

    for model_name in models_to_sync:
        model = django.apps.apps.get_model(app_label='api', model_name=model_name)
        
        # 로컬 DB에서 데이터 가져오기
        local_objects = model.objects.using('default').all()
        
        for obj in local_objects:
            # Heroku DB에 데이터 동기화
            model.objects.using('heroku_db').update_or_create(
                pk=obj.pk,
                defaults={field.name: getattr(obj, field.name) for field in obj._meta.fields if field.name != 'id'}
            )
        
        print(f"{model_name} 모델 동기화 완료")

if __name__ == "__main__":
    sync_data()