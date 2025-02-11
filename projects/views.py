from django.shortcuts import render


def project(request):
    return render(request, 'projects/project.html')
