from uuid import uuid4

from django.db import models
from users.models import Profile
from django.core.validators import FileExtensionValidator

from utils.validators import IMAGE_EXTENSIONS, size_validator
from utils.image_compression import compress_image

from users.models import Profile


def upload_to(instance, filename):
    return f'projects/{instance.id}/{filename}'


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='projects')

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    github_link = models.URLField(null=True, blank=True)
    demo_link = models.URLField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    @property
    def get_media(self):
        return self.media.all() if self.media.exists() else None


class ProjectMedia(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS.append('gif')),
            size_validator
        ]
    )
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['project']

    def __str__(self):
        return self.project.title
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file = compress_image(self.file)

        super().save(*args, **kwargs)


class Feature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name


class ProjectStats(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='project_stats')

    upvotes = models.PositiveIntegerField(default=0, blank=True)
    downvotes = models.PositiveIntegerField(default=0, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        verbose_name = 'Project Stats'
        verbose_name_plural = 'Project Stats'

    def __str__(self):
        return self.project.title
    
    @property
    def get_votes_ratio(self):
        ratio = self.upvotes - self.downvotes
        return ratio
    

class ProjectVote(models.Model):
    VOTE_TYPES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        unique_together = ('project', 'profile')
        verbose_name = 'Project vote'
        verbose_name_plural = 'Project votes'
        ordering = ['project', 'vote_type', 'created']

    def __str__(self):
        return self.vote_type


# class Tag(models.Model):
#     pass


# class ProjectTag(models.Model):
#     pass
