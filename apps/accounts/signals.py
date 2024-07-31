from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Функция приемника, которая запускается каждый раз при создании пользователя.
    Пользователь является отправителем, который несет ответственность за отправку уведомления."""
    if created:
        Profile.objects.create(user=instance)
