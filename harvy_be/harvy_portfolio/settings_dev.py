from .settings import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SECRET_KEY = 'django-insecure-733=d8zn2nu=b566a&28ip3iviw39=(x8k#7%69qks_heqlpq3'
DEBUG = True

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'postgres',
        'PASSWORD': 'tmdghl12#$',
        'HOST': 'localhost',
        'PORT': '5432',
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