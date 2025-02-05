import os
import shutil
from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            display_name=instance.username
        )


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        pass


@receiver(post_delete, sender=Profile)
def delete_profile_pic(sender, instance, **kwargs):
    try:
        profile = instance
        path = f'media/profiles/{profile.user.username}'
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        print(f'Error while deleting profile directory: {e}')