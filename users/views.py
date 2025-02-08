import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from .forms import *
from .models import *
from cities_light.models import City


def htmx_http_response(status_code: int, message: dict, event: str):
    return HttpResponse(
        status=status_code,
        headers={
            'HX-Trigger': json.dumps({
                event: None,
                'showMessage': message,
            })
        }
    )


@login_required(login_url='account_login')
def account(request):
    return render(request, 'users/account.html')


@login_required(login_url='account_login')
def profile_info(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'users/includes/profile_info.html', context)


@login_required(login_url='account_login')
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            message = {
                'text': 'Profile was updated',
                'type': 'success'
            }

            return htmx_http_response(204, message, event='profileInfoChanged')

    form = ProfileForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'users/edit_profile.html', context)


def load_cities(request):
    country_id = request.GET.get('country')

    if not country_id:
        return HttpResponse("<option value=''>No available cities for this region</option>")

    cities = City.objects.filter(country_id=country_id)

    if not cities.exists():
        return HttpResponse("<option value=''>No available cities for this region</option>")

    context = {
        'queryset': cities,
    }

    return render(request, 'users/obj_options.html', context)


def load_skills(request):
    category_id = request.GET.get('category')

    if not category_id:
        return HttpResponse("<option value=''>No available skills for this category</option>")
    
    skills = Skill.objects.filter(category_id=category_id)

    if not skills.exists():
        return HttpResponse("<option value=''>No available skills for this category</option>")
    
    context = {
        'queryset': skills,
    }

    return render(request, 'users/obj_options.html', context)


@login_required(login_url='account_login')
def skill_list(request):
    profile = request.user.profile
    skills = profile.skills.all()

    context = {
        'skills': skills,
    }

    return render(request, 'users/includes/skill_list.html', context)


@login_required(login_url='account_login')
def add_skill(request):
    if request.method == 'POST':
        form = ProfileSkillForm(request.POST)
        if form.is_valid():
            skill = form.cleaned_data.get('skill')
            profile = request.user.profile

            obj, created = ProfileSkill.objects.get_or_create(profile=profile, skill=skill)

            message = {
                'text': obj.name + ' was added' if created else 'is already added',
                'type': 'success' if created else 'danger'
            }

            return htmx_http_response(204, message, event='skillListChanged')

    form = ProfileSkillForm()

    context = {
        'form': form,
        'obj_name': 'Skill',
        'url': request.path
    }

    return render(request, 'users/obj_form.html', context)


@login_required(login_url='account_login')
def delete_skill(request, pk):
    skill = get_object_or_404(ProfileSkill, id=pk)

    if request.method == 'POST':
        skill.delete()

        message = {
            'text': f'{skill.name} was removed',
            'type': 'danger'
        }

        return htmx_http_response(204, message, event='skillListChanged')

    context = {
        'url': reverse('users:delete_skill', args=[skill.id]),
        'obj_name': 'Skill',
        'obj_name_value': skill.name,
    }

    return render(request, 'users/obj_delete.html', context)


@login_required(login_url='account_login')
def social_list(request):
    profile = request.user.profile
    socials = profile.socials.all()

    context = {
        'socials': socials,
    }

    return render(request, 'users/includes/social_list.html', context)


@login_required(login_url='account_login')
def add_social(request):
    if request.method == 'POST':
        form = ProfileSocialForm(request.POST)
        if form.is_valid():
            social = form.cleaned_data.get('social')
            profile = request.user.profile

            obj, created = ProfileSocial.objects.get_or_create(profile=profile, social=social)

            print('\n', obj.name, '\n')

            message = {
                'text': obj.name.capitalize() + ' link was added' if created else 'is already added',
                'type': 'success' if created else 'danger'
            }

            return htmx_http_response(204, message, event='socialListChanged')

    form = ProfileSocialForm()

    context = {
        'form': form,
        'obj_name': 'Social',
        'url': request.path,
    }

    return render(request, 'users/obj_form.html', context)


@login_required(login_url='account_login')
def delete_social(request, pk):
    social = get_object_or_404(ProfileSocial, id=pk)

    if request.method == 'POST':
        social.delete()

        message = {
            'text': f'{social.name.capitalize()} was removed',
            'type': 'danger'
        }

        return htmx_http_response(204, message, event='socialListChanged')
    
    context = {
        'url': reverse('users:delete_social', args=[social.id]),
        'obj_name': 'Social',
        'obj_name_value': social.name,
    }

    return render(request, 'users/obj_delete.html', context)
