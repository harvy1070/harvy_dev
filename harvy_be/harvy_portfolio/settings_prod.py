import os
import dj_database_url
from .settings import *
from urllib.parse import urlparse

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')
# Heroku 환경을 위한 Redis 설정
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
url = urlparse(REDIS_URL)

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'harvy-dev-f064f0b3b0ee.herokuapp.com,localhost,127.0.0.1,harvy.kr,www.harvy.kr,api.harvy.kr').split(',')

# heroku, db 연동용으로 수정
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True),
    'local_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Heroku DATABASE_URL이 설정되어 있지 않은 경우를 위한 폴백
if 'DATABASE_URL' not in os.environ:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('HEROKU_DB_NAME'),
        'USER': os.getenv('HEROKU_DB_USER'),
        'PASSWORD': os.getenv('HEROKU_DB_PASSWORD'),
        'HOST': os.getenv('HEROKU_DB_HOST'),
        'PORT': os.getenv('HEROKU_DB_PORT'),
}
    
DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

# DATABASES = {
#     'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
# }

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = []

if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE

CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'False') == 'True'
# CORS_ALLOWED_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'https://harvy13.netlify.app,https://harvy.kr,https://www.harvy.kr,https://api.harvy.kr').split(',')
# CORS_ALLOWED_ORIGINS = [
#     'https://harvy13.netlify.app',
#     'https://harvy.kr',
#     'https://www.harvy.kr',
#     'https://api.harvy.kr'
# ]

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SIMPLE_JWT = {**SIMPLE_JWT, 'SIGNING_KEY': SECRET_KEY}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'api': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'rq.worker': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Heroku 환경을 위한 RQ 설정 오버라이드
RQ_QUEUES = {
    'default': {
        'URL': REDIS_URL,
        'DEFAULT_TIMEOUT': 360,
    }
}

# 캐시 설정 업데이트
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}