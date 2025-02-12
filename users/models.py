from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from utils.validators import IMAGE_EXTENSIONS, size_validator
from cities_light.models import Country, City


def upload_to(instance, filename):
    return f'profiles/{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    display_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=150, null=True, blank=True)
    
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    
    about_info = models.TextField(null=True, blank=True)

    image = models.ImageField(
        default='default/default_pfp.png',
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS),
            size_validator
        ]
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.user.username
    
    def get_name(self):
        return self.display_name if self.display_name else self.user.username
    
    @property
    def get_username(self):
        return self.user.username
    
    def get_location(self):
        data = [
            self.city.name if self.city else None,
            self.country.name if self.country else None
        ]
        return ', '.join(filter(None, data))
    
    @property
    def get_skills(self):
        return self.skills.all()
    
    @property
    def get_socials(self):
        return self.socials.all()
    
    @property
    def get_projects(self):
        return self.projects.all()
    
    @property
    def get_bio(self):
        return self.bio if self.bio else ''


class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name
    

class ProfileSkill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        unique_together = ('profile', 'skill')

    def __str__(self):
        return self.profile.user.username
    
    @property
    def name(self):
        return self.skill.name
    

class Social(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name
    

class ProfileSocial(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='socials')
    social = models.ForeignKey(Social, on_delete=models.CASCADE)
    url = models.URLField(max_length=100, null=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        unique_together = ('profile', 'social')

    def __str__(self):
        return self.profile.get_username
    
    @property
    def name(self):
        return self.social.name
