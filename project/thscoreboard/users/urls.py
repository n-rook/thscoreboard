from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.register, name='register'),
    path('registration_success', views.registration_success, name='registration_success'),
    # For now, just reuse the built-in Django pages.
    path('', include('django.contrib.auth.urls')),
    
]
