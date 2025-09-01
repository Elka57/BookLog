
from allauth.account.views import ConfirmEmailView as BaseConfirmEmailView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.conf import settings

class ConfirmEmailAndLoginView(BaseConfirmEmailView):
    """
    1) Super-провайдер подтверждает email
    2) Через django.contrib.auth.login создаём сессию
    3) Делаем редирект на фронтенд-процессинг
    """
    def get(self, request, *args, **kwargs):
        # вызываем логику Allauth, чтобы confirmation_code отработал
        response = super().get(request, *args, **kwargs)

        # объект EmailAddress теперь уже подтверждён
        user = self.email_address.user

        # создаём sessionid-куку
        login(request, user)

        # редиректим на страницу фронтенда, где дальше поднимем профиль
        return redirect(f"{settings.FRONTEND_URL}/confirm-email/{kwargs['key']}")
