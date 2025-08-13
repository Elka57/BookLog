from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import User, UserTypes

@receiver(pre_save, sender=User)
def sync_user_flags(sender, instance, **kwargs):
    # STAFF → is_staff
    instance.is_staff = (instance.user_type == UserTypes.STAFF)
    # ADMIN → is_superuser
    instance.is_superuser = (instance.user_type == UserTypes.ADMIN)
