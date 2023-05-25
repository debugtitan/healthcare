from .models import BanPatient
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=BanPatient)
def set_default_values(sender, instance, created, **kwargs):
    if created:
        User = get_user_model()
        User.objects.filter(is_active=True).update(is_banned=False)
