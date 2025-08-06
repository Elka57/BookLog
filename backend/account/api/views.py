# account/api/views.py

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import EmailChangeRequestSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from account.models import EmailChangeRequest
from django.contrib.auth import get_user_model
from account.models import PasswordResetRequest


class EmailChangeViewSet(viewsets.GenericViewSet):
    serializer_class = EmailChangeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'token'
    queryset = EmailChangeRequest.objects.all()

    @action(methods=['post'], detail=False)
    def request(self, request):
        """Создать запрос на смену email + отправить письмо."""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        email_request = serializer.save()

        # Отправка письма
        link = f"{settings.FRONTEND_URL}/confirm-email/{email_request.token}/"
        subject = "Подтвердите смену email"
        body = (
            f"Здравствуйте, {request.user.get_full_name()}!\n\n"
            f"Чтобы подтвердить смену почты, перейдите по ссылке:\n{link}\n\n"
            "Если это были не вы — проигнорируйте это письмо."
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email_request.new_email])

        return Response({'detail': 'Письмо с подтверждением отправлено'}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path='confirm')
    def confirm(self, request):
        """Подтверждение смены email по токену."""
        token = request.data.get('token')
        req = get_object_or_404(EmailChangeRequest, token=token)

        if req.used:
            return Response({'detail': 'Запрос уже выполнен'}, status=status.HTTP_400_BAD_REQUEST)
        if req.is_expired:
            return Response({'detail': 'Срок действия ссылки истек'}, status=status.HTTP_400_BAD_REQUEST)

        # Меняем email и отмечаем использование
        user = req.user
        user.email = req.new_email
        user.save(update_fields=['email'])
        req.mark_used()

        return Response({'detail': 'Email успешно изменён'}, status=status.HTTP_200_OK)



User = get_user_model()


class PasswordResetViewSet(viewsets.GenericViewSet):
    queryset = PasswordResetRequest.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(methods=['post'], detail=False)
    def request(self, request):
        """Создать запрос на сброс пароля + отправить письмо."""
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_req = serializer.save()

        link = f"{settings.FRONTEND_URL}/reset-password/{reset_req.token}/"
        subject = "Сброс пароля"
        body = (
            f"Здравствуйте, {reset_req.user.get_full_name()}!\n\n"
            f"Чтобы сбросить пароль, перейдите по ссылке:\n{link}\n\n"
            "Если это были не вы — проигнорируйте это письмо."
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [reset_req.user.email])

        return Response({'detail': 'Письмо со ссылкой для сброса отправлено'}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path='confirm')
    def confirm(self, request):
        """Подтверждение сброса пароля."""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Пароль успешно сброшен'}, status=status.HTTP_200_OK)
