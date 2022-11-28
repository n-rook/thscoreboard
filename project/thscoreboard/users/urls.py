
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from users import other_views
from users.views import accept_invite
from users.views import batch_invite_csv
from users.views import profile

app_name = 'users'

urlpatterns = [
    path('register', other_views.register, name='register'),
    path('registration_success', other_views.registration_success, name='registration_success'),
    path('preregistered', other_views.preregistered, name='preregistered'),
    path('verify_email/<str:token>', other_views.verify_email, name='verify_email'),
    path('accept_invite/<str:token>', accept_invite.accept_invite, name='accept_invite'),
    path('profile', profile.profile, name='profile'),
    path('batch_invite', batch_invite_csv.batch_invite, name='batch_invite'),
    path('batch_invite_confirm', batch_invite_csv.batch_invite_confirm, name='batch_invite_confirm'),

    path(
        'login',
        auth_views.LoginView.as_view(),
        name='login'),
    path(
        'logout',
        auth_views.LogoutView.as_view(),
        name='logout'),
    path(
        'forgot_password',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('users:forgot_password_sent')
        ),
        name='forgot_password'
    ),
    path(
        'forgot_password/sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_sent.html'
        ),
        name='forgot_password_sent',
    ),
    path(
        "forgot_password/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('users:forgot_password_complete')
        ),
        name="forgot_password_confirm",
    ),
    path(
        "forgot_password/done/",
        auth_views.PasswordResetCompleteView.as_view(
        ),
        name="forgot_password_complete",
    ),
]
