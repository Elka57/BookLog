from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.api.views import EmailChangeViewSet, PasswordResetViewSet

router_account_actions = DefaultRouter()
router_account_actions.register(r'email-change', EmailChangeViewSet, basename='email-change')
router_account_actions.register(r'password-reset', PasswordResetViewSet, basename='password-reset')

urlpatterns = [
    path('account_actions/', include(router_account_actions.urls)),
]
