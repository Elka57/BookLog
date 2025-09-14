from django.db.models.signals import pre_save
from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from users.models import User, UserTypes
print("Файл сигналов импортирован")

@receiver(pre_save, sender=User)
def sync_user_flags(sender, instance, **kwargs):
    # STAFF → is_staff
    instance.is_staff = (instance.user_type == UserTypes.STAFF)
    # ADMIN → is_superuser
    instance.is_superuser = (instance.user_type == UserTypes.ADMIN)


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    print("Мы в сигнале = on_email_confirmed и у нас email_address = ", email_address)
    print("Ищем пользователя")
    user = User.objects.get(email=email_address)
    print("Вот ккого пользователя мы нашли = ", user)
    user.email_confirmed = True
    user.save(update_fields=["email_confirmed"])
