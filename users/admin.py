from django.contrib import admin
from .models import *


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'created']
