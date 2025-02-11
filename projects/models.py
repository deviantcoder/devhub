from uuid import uuid4

from django.db import models
from users.models import Profile


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    github_link = models.URLField(null=True, blank=True)
    demo_link = models.URLField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


# class ProjectMedia(models.Model):
#     pass


# class Feature(models.Model):
#     pass


# class ProjectStats(models.Model):
#     pass


# class ProjectTags(models.Model):
#     pass
