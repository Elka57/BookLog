from .base import *

DEBUG = True

# Разрешить все локальные хосты
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Dev-зависимости
INSTALLED_APPS += [
    'django_extensions',
    'pytest_django',
    'rest_framework.authtoken',
]

# Консольный e-mail
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Дополнительные настройки CORS
CORS_ALLOW_ALL_ORIGINS = True
