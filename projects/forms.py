from django import forms
from django.forms import inlineformset_factory
from .models import Project, ProjectMedia


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'demo_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


ProjectMediaFormSet = inlineformset_factory(
    Project,
    ProjectMedia,
    fields=['file'],
    extra=1,
    can_delete=True
)