import re
from rest_framework import serializers
from ..models import User, UserTypes

from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.core.validators import EmailValidator

from allauth.account.models import EmailAddress

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
        fields = ['id', 'username', 'name', 'email', 'email_confirmed', 'logo', 'user_type']
        read_only_fields = ['id', 'username', 'email_confirmed']


    def update(self, instance, validated_data):

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


    # app/serializers.py
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class UsernameOrEmailLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        try:
          EmailValidator()(username)
          is_email = True
        except Exception:
          is_email = False
        if not username or not password:
            raise serializers.ValidationError(
                "Введите username или email и пароль."
            )

        if is_email:
          try:
              u = User.objects.get(email__iexact=username)
              user = authenticate(username=u.username, password=password)
          except User.DoesNotExist:
              user = None
        else:
            user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                "Неверные учётные данные."
            )
        attrs["user"] = user
        return attrs



class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=False)
    user_type = serializers.ChoiceField(choices=UserTypes.choices)
    logo = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        print("Мы в customRegisterSerializer в get_cleaned_data и вот какие данные = ", )
        data = super().get_cleaned_data()
        print(self.validated_data)
        data['name'] = self.validated_data.get('name', '')
        data['user_type'] = self.validated_data.get('user_type')
        data['logo'] = self.validated_data.get('logo')
        return data

    def save(self, request):
        print("Мы в customRegisterSerializer в save")
        user = super().save(request)  # здесь создаются username/email/password
        user.name = self.cleaned_data.get('name', '')
        print("У нас в save user_type = ", self.cleaned_data.get('user_type'))
        user.user_type = self.cleaned_data.get('user_type')
        print("И в пользователе сохраняем = ", user.user_type)
        if self.cleaned_data.get('logo'):
            user.logo = self.cleaned_data.get('logo')
        user.save()
        print("Мы в CustomRegisterSerializer и у нас user = ", user)
        print("А вот и лого в пользователе = ", user.logo)
        print("А еще у нас че по подтвержденному емейлу = ", user.email_confirmed)
        return user


        
  