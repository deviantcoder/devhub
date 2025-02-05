from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile


@login_required(login_url='account_login')
def account(request):
    profile = request.user.profile

    context = {
        'profile': profile
    }

    return render(request, 'users/account.html', context)
