from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
from .models import *
from cities_light.models import City


@login_required(login_url='account_login')
def account(request):
    profile = request.user.profile
    context = {
        'profile': profile,
    }

    return render(request, 'users/account.html', context)


def skill_list(request):
    profile = request.user.profile
    skills = profile.skills.all()

    context = {
        'skills': skills,
    }

    return render(request, 'users/includes/skill_list.html', context)


@login_required(login_url='account_login')
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was updated')
            return redirect('/')

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
        'cities': cities,
    }

    return render(request, 'users/city_options.html', context)


@login_required(login_url='account_login')
def add_skill(request):
    if request.method == 'POST':
        form = ProfileSkillForm(request.POST)
        if form.is_valid():
            skill = form.cleaned_data.get('skill')
            profile = request.user.profile

            obj, created = ProfileSkill.objects.get_or_create(profile=profile, skill=skill)

            if created:
                messages.success(request, f'{obj.name} was added')
            else:
                messages.warning(request, f'{obj.name} is already added')

            return HttpResponse(status=204, headers={'HX-Trigger': 'skillListChanged'})

    form = ProfileSkillForm()

    context = {
        'form': form
    }

    return render(request, 'users/skill_form.html', context)


@login_required(login_url='account_login')
def delete_skill(request, pk):
    skill = get_object_or_404(ProfileSkill, id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted')
        return HttpResponse(status=204, headers={'HX-Trigger': 'skillListChanged'})

    context = {
        'skill': skill
    }

    return render(request, 'users/delete_skill.html', context)
