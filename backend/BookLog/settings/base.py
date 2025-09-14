from pathlib import Path
from decouple import config, Csv
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность и хосты
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())
TIME_ZONE = config('TIME_ZONE', default='UTC')

# Приложения
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'rest_framework_roles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    # Ваши приложения
    "users.apps.UsersConfig",
    'authentication',
    'journal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BookLog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'BookLog.wsgi.application'

# База данных
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     config('POSTGRES_DB'),
        'USER':     config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST':     config('DB_HOST', default='db'),
        'PORT':     config('DB_PORT', default=5432, cast=int),
    }
}

# Авто-поля, локализация, время
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'ru'
USE_I18N = True
USE_TZ = True

# Статика и медиа
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# REST framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT
# dj-rest-auth
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'booklog-app-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'booklog-refresh-token',

    'LOGIN_SERIALIZER':  'users.api.serializers.UsernameOrEmailLoginSerializer',
    'REGISTER_SERIALIZER': 'users.api.serializers.CustomRegisterSerializer',
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    #'ROTATE_REFRESH_TOKENS': True,
    #'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Пользователь
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False
ACCOUNT_ADAPTER = 'users.adapters.FrontendAccountAdapter'

ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = config('FRONTEND_URL')
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = config('FRONTEND_URL')

PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = f"{config('FRONTEND_URL')}/password-reset/confirm"
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False

# Логирование, токены удаления профиля и роли
PROFILE_DELETION_TOKEN_EXPIRY = 24 * 3600
REST_FRAMEWORK_ROLES = {
    'ROLES': 'BookLog.roles.ROLES',
    'DEFAULT_EXCEPTION_CLASS': 'rest_framework.exceptions.NotFound',
}

# CORS / CSRF
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [config('FRONTEND_URL')]
CORS_ALLOW_METHODS = ("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT")
CSRF_TRUSTED_ORIGINS = [config('FRONTEND_URL')]
CSRF_COOKIE_HTTPONLY = False


FRONTEND_URL = config('FRONTEND_URL')
