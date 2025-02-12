from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('project/', views.project, name='project'),
    path('project-list/', views.project_list, name='project_list'),

    path('add-project/', views.add_project, name='add_project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete_project'),
]