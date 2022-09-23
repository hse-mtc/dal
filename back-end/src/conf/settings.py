"""
Django settings for DAL project.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ["DEBUG"].lower() == "true"

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Addons
    "corsheaders",
    "dbbackup",
    "django_filters",
    "drf_spectacular",
    "ordered_model",
    "taggit",
    # REST framework
    "rest_framework",
    "rest_framework.authtoken",
    # DAL apps
    "auth",
    "common",
    "ams",
    "dms",
    "lms",
    "tgbot",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "silk",
    ]

MIDDLEWARE = [
    "common.middleware.LoggingMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE = (
        [
            "common.middleware.LoggingMiddleware",
        ]
        + MIDDLEWARE
        + [
            "silk.middleware.SilkyMiddleware",
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]
    )

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    }
}

# Database backups

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {
    "location": BASE_DIR / "backups",
}
DBBACKUP_CONNECTORS = {
    "default": {
        "CONNECTOR": "dbbackup.db.postgresql.PgDumpBinaryConnector",
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# REST framework settings

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "auth.permissions.ReadOnly",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# Media files (uploaded by users)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CORS configuration

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# taggit configuration

TAGGIT_CASE_INSENSITIVE = True

# Debug Toolbar settings

INTERNAL_IPS = [
    "127.0.0.1",
]

# JWT authentication settings

BEARER_AUTH_HEADER_TYPE = "Bearer"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": [BEARER_AUTH_HEADER_TYPE],
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ["rest_framework_simplejwt.tokens.AccessToken"],
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Max size for request data and files

BYTES_IN_MEGABYTE = 1024 * 1024
# Data may contain base64 images
DATA_UPLOAD_MAX_MEMORY_SIZE = 80 * BYTES_IN_MEGABYTE  # 80 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 80 * BYTES_IN_MEGABYTE  # 80 MB

# Default lifetime for registration confirmation token

REGCONF_TOKEN_LIFETIME = timedelta(days=10)

# Custom user model

AUTH_USER_MODEL = "dal_auth.User"

# DAL services

WATCHDOC_HOST = os.environ["WATCHDOC_HOST"]
WATCHDOC_PORT = os.environ["WATCHDOC_PORT"]

TGBOT_HOST = os.environ["TGBOT_HOST"]
TGBOT_PORT = os.environ["TGBOT_PORT"]
TGBOT_EMAIL = os.environ["TGBOT_EMAIL"]
TGBOT_PASSWORD = os.environ["TGBOT_PASSWORD"]

# Swagger settings for drf-spectacular

SPECTACULAR_SETTINGS = {
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",
        "filter": True,
        "persistAuthorization": True,
    },
    # Meta info
    "TITLE": "DAL REST API",
    "DESCRIPTION": "API for auth, dms, lms apps",
    "VERSION": "0.7.0",
    # Enum namings
    "ENUM_NAME_OVERRIDES": {
        # ----------------------------------------------------------------------
        # common
        "RelativeType": "common.models.personal.Relative.Type",
        "Campus": "common.models.universities.Campus",
        # ----------------------------------------------------------------------
        # auth
        "PermissionScope": "auth.models.Permission.Scope",
        # ----------------------------------------------------------------------
        # ams
        "MedicalExamination": "ams.models.applicants.ApplicationProcess.MedicalExamination",
        "ProfPsySelection": "ams.models.applicants.ApplicationProcess.ProfPsySelection",
        # ----------------------------------------------------------------------
        # dms
        "ClassMaterialType": "dms.models.class_materials.ClassMaterial.Type",
        # ----------------------------------------------------------------------
        # lms
        "AbsenceExcuse": "lms.models.absences.Absence.Excuse",
        "AbsenceStatus": "lms.models.absences.Absence.Status",
        "EncouragementType": "lms.models.encouragements.Encouragement.Type",
        "LessonType": "lms.models.lessons.Lesson.Type",
        "PunishmentType": "lms.models.punishments.Punishment.Type",
        "StudentStatus": "lms.models.students.Student.Status",
        "StudentPost": "lms.models.students.Student.Post",
        "TeacherRank": "lms.models.teachers.Teacher.Rank",
        "TeacherPost": "lms.models.teachers.Teacher.Post",
        "UniformHeaddress": "lms.models.uniforms.Uniform.Headdress",
        "UniformOuterwear": "lms.models.uniforms.Uniform.Outerwear",
    },
}

# Logging settings

LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            "style": "%",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": True,
        },
        "dal.logging": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Email settings

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"].lower() == "true"
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_FROM_NAME = "Даль ВУЦ ВШЭ"
DEFAULT_FROM_EMAIL = f"{EMAIL_FROM_NAME} <{EMAIL_HOST_USER}>"

# Settings used for tests

TEST_CORPORATE_EMAIL_DOMAIN = "thisistestemaildomain.org"
