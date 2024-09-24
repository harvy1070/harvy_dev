import os
from .settings import *
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 환경 변수에서 SECRET_KEY 가져오기
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = True

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    },
    'heroku_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('HEROKU_DB_NAME'),
        'USER': os.getenv('HEROKU_DB_USER'),
        'PASSWORD': os.getenv('HEROKU_DB_PASSWORD'),
        'HOST': os.getenv('HEROKU_DB_HOST'),
        'PORT': os.getenv('HEROKU_DB_PORT'),
    }
}

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Override SIMPLE_JWT settings if needed
SIMPLE_JWT = {**SIMPLE_JWT, 'SIGNING_KEY': SECRET_KEY}

# 개발 환경에서의 Redis 설정
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    }
}