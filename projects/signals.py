from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Project, ProjectStats


@receiver(signal=post_save, sender=Project)
def create_poststats(sender, instance, created, **kwargs):
    if created:
        ProjectStats.objects.create(project=instance)