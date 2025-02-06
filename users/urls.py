from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.account, name='account'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('load_cities/', views.load_cities, name='load_cities'),
]