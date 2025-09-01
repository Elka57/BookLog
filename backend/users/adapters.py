# users/adapters.py

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class FrontendAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        # эта ссылка придёт в письме сразу на фронтенд
        return f"{settings.FRONTEND_URL}/confirm-email/{emailconfirmation.key}"
