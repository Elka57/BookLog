from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,        
        blank=True,
        null=True
    )
    email_confirmed = models.BooleanField(
        verbose_name="E-mail подтверждён",
        default=False
    )
    logo = models.ImageField(
        verbose_name="Картинка профиля",
        upload_to="user_logos/",  
        blank=True,
        null=True
    )

    def __str__(self):
        return self.get_full_name() or self.username


