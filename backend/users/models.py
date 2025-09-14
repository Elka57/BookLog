
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserTypes(models.IntegerChoices):
    JOURNALIST = 0, "Журналист"
    READER = 1, "Читатель"
    STAFF = 2, "Модератор"
    ADMIN = 3, "Администратор"

class User(AbstractUser):
    name = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,        
        blank=True,
        null=True
    )
    logo = models.ImageField(
        verbose_name="Картинка профиля",
        upload_to="user_logos/",  
        blank=True,
        null=True
    )
    email_confirmed = models.BooleanField(
        verbose_name="Статус подтверждения электронной почты", 
        default=False
        )
    user_type = models.IntegerField(choices=UserTypes.choices, verbose_name="Тип", default=UserTypes.READER)

    def __str__(self):
        return self.get_full_name() or self.username
