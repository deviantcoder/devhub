from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'location', 'created']
    formfield_overrides = {
        models.ManyToManyField: {
            'widget': CheckboxSelectMultiple
        }
    }

    def location(self, obj):
        return obj.get_location()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


class SkillInline(admin.StackedInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    inlines = [SkillInline]
