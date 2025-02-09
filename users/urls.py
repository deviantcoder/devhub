from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('account/', views.account, name='account'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.profiles, name='profiles'),

    path('profile-info/', views.profile_info, name='profile_info'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile-overview/<str:pk>/', views.profile_overview, name='profile_overview'),

    path('load_cities/', views.load_cities, name='load_cities'),

    path('skill-list/', views.skill_list, name='skill_list'),
    path('load_skills/', views.load_skills, name='load_skills'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete_skill'),

    path('social-list/', views.social_list, name='social_list'),
    path('add-social/', views.add_social, name='add_social'),
    path('delete-social/<str:pk>/', views.delete_social, name='delete_social'),
]