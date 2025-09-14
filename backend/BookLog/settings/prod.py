from .base import *

DEBUG = False

# ALLOWED_HOSTS задаётся через .env
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Удаляем dev-приложения, если они попали из base
for app in ('django_extensions', 'pytest_django', 'rest_framework.authtoken'):
    if app in INSTALLED_APPS:
        INSTALLED_APPS.remove(app)

# SMTP для реальной отправки почты
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST          = config('EMAIL_HOST')
EMAIL_PORT          = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER     = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS       = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL  = config('DEFAULT_FROM_EMAIL')

# Безопасные cookie и HTTPS
SECURE_SSL_REDIRECT          = True
SESSION_COOKIE_SECURE        = True
CSRF_COOKIE_SECURE           = True
SECURE_HSTS_SECONDS          = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD          = True
