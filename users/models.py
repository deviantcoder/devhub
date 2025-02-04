from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


def upload_to(instance, filename):
    return f'profiles/{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    display_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    
    about_info = models.TextField(null=True, blank=True)

    image = models.ImageField(default='default/default_pfp.png', upload_to=upload_to)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.user.username
    
    def get_name(self):
        return self.display_name if self.display_name else self.user.username