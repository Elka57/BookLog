from rest_framework import serializers
from ..models import User

from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(
        use_url=True,
        allow_null=True,
        required=False
    )
    email = serializers.EmailField(
        required=False
    )

    class Meta:
        model = User
        # Разрешаем менять только эти поля
        fields = ['id', 'username', 'name', 'email', 'email_confirmed', 'logo']
        read_only_fields = ['id', 'username', 'email_confirmed']

    def update(self, instance, validated_data):
        # 1. Обновляем email и сбрасываем флаг подтверждения
        new_email = validated_data.get('email')
        if new_email and new_email != instance.email:
            instance.email = new_email
            instance.email_confirmed = False
            # Здесь при необходимости можете вызвать отправку письма

        # 2. Обновляем имя
        if 'name' in validated_data:
            instance.name = validated_data['name']

        # 3. Обновляем аватар
        if 'logo' in validated_data:
            instance.logo = validated_data['logo']

        instance.save()
        return instance


class ProfileDeletionConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()