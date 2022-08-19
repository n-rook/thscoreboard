
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.register, name='register'),
    path('registration_success', views.registration_success, name='registration_success'),

    path(
        'login',
        auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='login'),
    path(
        'logout',
        auth_views.LogoutView.as_view(),
        {'template_name': 'registration/logout2.html'},
        name='logout'),
]
