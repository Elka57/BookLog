from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from ..models import EmailChangeRequest, PasswordResetRequest, User

from django.contrib.auth import get_user_model


User = get_user_model()

class EmailChangeRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    token = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    used = serializers.BooleanField(read_only=True)
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = EmailChangeRequest
        fields = [
            'id',
            'user',
            'new_email',
            'token',
            'created_at',
            'used',
            'is_expired',
        ]

    def get_is_expired(self, obj):
        return obj.is_expired

    def validate_new_email(self, value):
        user = self.context['request'].user
        if user.email == value:
            raise serializers.ValidationError(
                "Новый email совпадает с текущим."
            )
        # Дополнительная проверка: не было ли уже активного запроса на тот же email
        exists = EmailChangeRequest.objects.filter(
            user=user,
            new_email=value,
            used=False,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).exists()
        if exists:
            raise serializers.ValidationError(
                "Уже отправлен запрос на этот email в последние 24 часа."
            )
        return value


class PasswordResetRequestSerializer(serializers.ModelSerializer):
    # Если reset по email, а не по аутентифицированному юзеру:
    email = serializers.EmailField(write_only=True)
    token = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    used = serializers.BooleanField(read_only=True)
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = PasswordResetRequest
        fields = [
            'id',
            'email',
            'token',
            'created_at',
            'used',
            'is_expired',
        ]

    def get_is_expired(self, obj):
        return obj.is_expired

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email не найден."
            )
        return value

    def create(self, validated_data):
        user = User.objects.get(email=validated_data.pop('email'))
        # Здесь можно отметить предыдущие unused-запросы устаревшими,
        # или сразу маркировать их used=True
        return PasswordResetRequest.objects.create(user=user)


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    re_new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        # 1) Пароли совпадают?
        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError({
                're_new_password': 'Пароли не совпадают'
            })

        # 2) Запрос сброса существует?
        try:
            reset_req = PasswordResetRequest.objects.get(token=attrs['token'])
        except PasswordResetRequest.DoesNotExist:
            raise serializers.ValidationError({
                'token': 'Неверный или несуществующий токен'
            })

        # 3) Уже использован?
        if reset_req.used:
            raise serializers.ValidationError({
                'token': 'Этот токен уже использован'
            })

        # 4) Просрочен?
        # Предполагаем, что в модели есть свойство `is_expired`
        if reset_req.is_expired:
            raise serializers.ValidationError({
                'token': 'Срок действия токена истёк'
            })

        # Всё ок — сохраняем объект для метода `save()`
        attrs['reset_req'] = reset_req
        return attrs

    def save(self, **kwargs):
        reset_req = self.validated_data['reset_req']
        user = reset_req.user
        new_password = self.validated_data['new_password']

        # Меняем пароль пользователя
        user.set_password(new_password)
        user.save()

        # Отмечаем запрос сброса как использованный
        reset_req.used = True
        reset_req.used_at = timezone.now()  # если есть поле used_at
        reset_req.save()

        return user
