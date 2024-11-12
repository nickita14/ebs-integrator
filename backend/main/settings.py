import os
from pathlib import Path

from .utils import env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.get_str('SECRET_KEY', '')

DEBUG = env.get_bool('DEBUG', False)

CSRF_TRUSTED_ORIGINS = env.get_list('CSRF_TRUSTED_ORIGINS', [])
CORS_ORIGIN_WHITELIST = env.get_list('CORS_ORIGIN_WHITELIST', [])

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'drf_standardized_errors',
    'main.apps.MainConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

CHANNEL_LAYERS = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.get_str('DB_NAME'),
        'HOST': env.get_str('DB_HOST'),
        'USER': env.get_str('DB_USER'),
        'PASSWORD': env.get_str('DB_PASSWORD'),
        'PORT': env.get_str('DB_PORT'),

    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.get_str('DB_NAME'),
        'HOST': env.get_str('DB_HOST'),
        'USER': env.get_str('DB_USER'),
        'PASSWORD': env.get_str('DB_PASSWORD'),
        'PORT': env.get_str('DB_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_standardized_errors.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'EBS Integrator API',
    'DESCRIPTION': 'Provides API for EBS Integrator app.',
    'VERSION': '1.0',
    'SCHEMA_PATH_PREFIX': '/api/v1',
    # Set to True if you want to serve the schema file with GET request,
    # otherwise specify a path where it can be accessed.
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVERS': [
        {
            'url': '{schema}://{hostname}',
            'description': 'Custom Server',
            'variables': {
                'schema': {
                    'default': 'http',
                    'enum': ['http', 'https'],
                    'description': 'Server URI schema.',
                },
                'hostname': {
                    'default': 'localhost',
                    'description': 'Server URI authority (can contain hostname and port).',
                },
            },
        },
        {'url': '/', 'description': 'Current Server'},
        {'url': 'http://localhost', 'description': 'Local Server'},
        {'url': 'https://example.com', 'description': 'Production Server'},
    ],
    'SWAGGER_UI_CONFIG': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,
        'defaultModelsExpandDepth': 2,
    },
    'POSTPROCESSING_HOOKS': ['drf_standardized_errors.openapi_hooks.postprocess_schema_enums'],
    'ENUM_NAME_OVERRIDES': {
        'ValidationErrorEnum': 'drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices',
        'ClientErrorEnum': 'drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices',
        'ServerErrorEnum': 'drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices',
        'ErrorCode401Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices',
        'ErrorCode403Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices',
        'ErrorCode404Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices',
        'ErrorCode405Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices',
        'ErrorCode406Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices',
        'ErrorCode415Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices',
        'ErrorCode429Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices',
        'ErrorCode500Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices',
    },
    'COMPONENT_SPLIT_REQUEST': True,
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = env.get_str('TZ', 'Europe/Chisinau')

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/api/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/api/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
