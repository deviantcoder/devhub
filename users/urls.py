from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.account, name='account'),
    path('profile-info/', views.profile_info, name='profile_info'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('load_cities/', views.load_cities, name='load_cities'),

    path('skill-list/', views.skill_list, name='skill_list'),
    path('load_skills/', views.load_skills, name='load_skills'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete_skill'),

    path('social-list/', views.social_list, name='social_list'),
    path('add-social/', views.add_social, name='add_social'),
    path('delete-social/<str:pk>/', views.delete_social, name='delete_social'),
]