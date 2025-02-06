from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile
from .forms import *
from cities_light.models import City


@login_required(login_url='account_login')
def account(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }

    return render(request, 'users/account.html', context)


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