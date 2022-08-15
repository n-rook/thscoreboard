from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register')
]