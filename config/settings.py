"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "o5s)wlwcy!xufd_ryiw2c=10p@0)%a@(2&g$mb3j5z1ohu(rze"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["airbnb-clone.eba-spnmfasu.ap-northeast-2.elasticbeanstalk.com"]

# Application definition

# 장고가 우리가 만든 폴더를 인식하게 하려면 밑에 처럼 작업이 필요하다
# PROJECT_APPS에 추가 시켜줌. 그리고 기본 APPS와 더해서 ISTALLED_APPS를 정의해줬음
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_countries",
    "django_seed",
]

PROJECT_APPS = [
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "core.apps.CoreConfig",
    "reviews.apps.ReviewsConfig",
    "reservations.apps.ReservationsConfig",
    "lists.apps.ListsConfig",
    "conversations.apps.ConversationsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# 이건 url을 나타낸다
STATIC_URL = "/static/"
# 이건 directory를 나타낸다
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# 우리가 만든 User 클래스를 쓰려고 AUTH_USER_MODEL을 바꿔줌
AUTH_USER_MODEL = "users.User"

# 사진이나 영상을 어디에 저장해놓을지 지정해줌
# 경로는 위에 BASE_DIR에서 가져왔다
# 이렇게 미디어파일 저장 경로를 설정해주면 uploads 폴더가 하나 생긴다
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# 미디어 파일의 경로를 인터넷 주소상 절대경로로 설정한다
MEDIA_URL = "/media/"


# Email Configration
# mailgun.com 에서 API정보를 받아와서 붙여넣는다
# sending - domain settings - SMTP credentials
# 이대로 올려버리면 Github에서 다른 사람이 내 password를 볼 수 있으니까 이걸 다른 곳에 올리고 불러와야한다
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = "587"
EMAIL_HOST_USER = os.environ.get("MAILGUN_USERNAME")
# PASSWORD는 우측 상단에 NEW SMTP USER를 생성해서 받아서 입력한다
# 다시는 얻을 수 없는 고유한 코드이다
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_PASSWORD")
# 메일 보내는 사람 지정
EMAIL_FROM = "good-boy@sandboxca116bc21a9448deb0176d60fb45ba25.mailgun.org"


# Auth
LOGIN_URL = "/users/login/"

# Locale 장고번역기 사용(translator)
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
