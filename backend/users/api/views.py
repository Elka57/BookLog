# account/api/views.py

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny

from users.utils import generate_deletion_token, verify_deletion_token
from users.models import User
from users.api.serializers import ProfileDeletionConfirmSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = UserSerializer

    def get_queryset(self):
        # Разрешаем видеть только свой профиль
        return User.objects.filter(pk=self.request.user.pk)

    def get_permissions(self):
        # POST /user/ — любой может зарегистрироваться
        if self.action == 'create':
            return [AllowAny()]
        # GET/PATCH /user/current/ и т.п. — только аутентифицированные
        return [IsAuthenticated()]


    @action(detail=False, methods=['get', 'patch'], url_path='current')
    def current(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProfileDeleteViewSet(viewsets.GenericViewSet):
    """
    1) POST /profile-delete/request/  — выслать письмо с токеном
    2) POST /profile-delete/confirm/  — подтвердить и удалить
    """
    serializer_class = ProfileDeletionConfirmSerializer

    def get_permissions(self):
        if self.action == 'request_deletion':
            return [IsAuthenticated()]
        if self.action == 'confirm_deletion':
            return [AllowAny()]
        return super().get_permissions()

    @action(
        detail=False,
        methods=['post'],
        url_path='request',
        url_name='request'
    )
    def request_deletion(self, request):
        user = request.user
        token = generate_deletion_token(user)

        confirm_url = (
            f"{settings.FRONTEND_URL.rstrip('/')}"
            f"/profile/delete/confirm?token={token}"
        )

        subject = "Подтвердите удаление профиля"
        message = (
            f"Здравствуйте, {user.get_full_name() or user.username}!\n\n"
            f"Чтобы удалить свой профиль, перейдите по ссылке:\n"
            f"{confirm_url}\n\n"
            f"Ссылка действительна "
            f"{settings.PROFILE_DELETION_TOKEN_EXPIRY // 3600} час(ов)."
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response(
            {"detail": "Письмо с ссылкой для удаления отправлено."},
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['post'],
        url_path='confirm',
        url_name='confirm'
    )
    def confirm_deletion(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        try:
            user_pk = verify_deletion_token(token)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, pk=user_pk)
        user.delete()

        return Response(
            {"detail": "Профиль успешно удалён."},
            status=status.HTTP_200_OK
        )