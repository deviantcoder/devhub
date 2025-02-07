import uuid
from django import forms
from allauth.account.forms import LoginForm, SignupForm
from django.forms import inlineformset_factory
from .models import *
from cities_light.models import Country, City


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })


class ProfileForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'hx-get': '/load_cities/',
            'hx-target': '#id_city',
        })
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False  
    )

    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'country', 'city', 'about_info', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        if 'country' in self.data and self.data.get('country'):
            country_id = int(self.data.get('country'))
            self.fields['city'].queryset = City.objects.filter(country_id=country_id)
        elif self.instance and self.instance.pk and self.instance.country:
            self.fields['city'].queryset = City.objects.filter(country=self.instance.country)
            self.initial['city'] = self.instance.city


class ProfileSkillForm(forms.ModelForm):
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = ProfileSkill
        fields = ['skill']