from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Project
from .forms import ProjectForm
from utils.htmx_response import htmx_http_response


def project(request):
    return render(request, 'projects/project.html')


@login_required(login_url='account_login')
def project_list(request):
    profile = request.user.profile
    projects = profile.get_projects

    context = {
        'projects': projects,
    }

    return render(request, 'projects/includes/project_list.html', context)


@login_required(login_url='account_login')
def add_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = request.user.profile
            project.save()

            message = {
                'text': 'Project was added',
                'type': 'success',
            }

            return htmx_http_response(204, message, event='projectsChanged')

    context = {
        'form': form,
        'page': 'Add',
        'url': reverse('projects:add_project')
    }

    return render(request, 'projects/project_form.html', context)


@login_required(login_url='account_login')
def edit_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()

            message = {
                'text': f'{project.title} was changed',
                'type': 'success'
            }

            return htmx_http_response(204, message, event='projectsChanged')

    context = {
        'form': form,
        'page': 'Edit',
        'url': reverse('projects:edit_project', args=[project.id])
    }

    return render(request, 'projects/project_form.html', context)


@login_required(login_url='account_login')
def delete_project(request, pk):
    project = get_object_or_404(Project, id=pk)

    if request.method == 'POST':
        project.delete()

        message = {
            'text': f'{project.title} was removed',
            'type': 'danger'
        }

        return htmx_http_response(204, message, event='projectsChanged')

    context = {
        'url': reverse('projects:delete_project', args=[project.id]),
        'obj_name': 'Project',
        'obj_name_value': project.title,
    }

    return render(request, 'obj/obj_delete.html', context)
