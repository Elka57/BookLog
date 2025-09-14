# myapp/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class FrontendAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        # ссылка сразу на SPA
        return (
          f"{settings.FRONTEND_URL}/confirm-email/{emailconfirmation.key}"
        )
