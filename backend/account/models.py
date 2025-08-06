import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

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


class EmailChangeRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="email_change_requests"
    )
    new_email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def mark_used(self):
        self.used = True
        self.save(update_fields=["used"])

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)

    def __str__(self):
        return f"{self.user} → {self.new_email} [{self.token}]"

    class Meta:
      ordering = ['-created_at']
      indexes = [
          models.Index(fields=['token']),
          models.Index(fields=['created_at']),
      ]
      unique_together = ('user', 'new_email', 'used')
      verbose_name = "Запрос на смену email"  # или "Смена email"
      verbose_name_plural = "Запросы на смену email"

    
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_requests"
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def mark_used(self):
        self.used = True
        self.save(update_fields=["used"])

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)

    def __str__(self):
        return f"{self.user} [{self.token}]"
    
    class Meta:
      ordering = ['-created_at']
      indexes = [
          models.Index(fields=['token']),
          models.Index(fields=['created_at']),
      ]
      unique_together = ('user', 'used')
      verbose_name = "Запрос на сброс пароля"
      verbose_name_plural = "Запросы на сброс пароля"

