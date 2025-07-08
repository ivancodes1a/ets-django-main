from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profileView, name='profile'),
    path('edit/', views.editProfile, name='editProfile'),
]