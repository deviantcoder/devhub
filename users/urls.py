from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.account, name='account'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile-info/', views.profile_info, name='profile_info'),
    path('load_cities/', views.load_cities, name='load_cities'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('skill-list/', views.skill_list, name='skill_list'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete_skill'),
]