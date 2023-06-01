from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from users.middleware import check_ban
from users import other_views
from users.views import (
    accept_invite,
    batch_invite_csv,
    banned,
    delete_account,
    profile,
    rankings,
    register,
    claim,
    set_language,
    my_claims,
)

from thscoreboard import settings

app_name = "users"

urlpatterns = [
    path("register", register.register, name="register"),
    path(
        "registration_success",
        register.registration_success,
        name="registration_success",
    ),
    path("preregistered", register.preregistered, name="preregistered"),
    path("verify_email/<str:token>", register.verify_email, name="verify_email"),
    path(
        "accept_invite/<str:token>", accept_invite.accept_invite, name="accept_invite"
    ),
    path("profile", profile.profile, name="profile"),
    path("delete_account", delete_account.delete_account, name="delete_account"),
    path("batch_invite", batch_invite_csv.batch_invite, name="batch_invite"),
    path(
        "batch_invite_confirm",
        batch_invite_csv.batch_invite_confirm,
        name="batch_invite_confirm",
    ),
    path("banned", banned.banned_notification, name="banned"),
    path("ip_bans/", other_views.view_ip_bans),
    path("ip_bans/add", other_views.add_ip_ban),
    path("ip_bans/<int:ban_id>/delete", other_views.delete_ip_ban),
    path("staff_ban", banned.staff_ban, name="staff_ban"),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path(
        "logout",
        check_ban.allow_access_by_banned_users(auth_views.LogoutView.as_view()),
        name="logout",
    ),
    path(
        "change_password",
        auth_views.PasswordChangeView.as_view(),
        name="change_password",
    ),
    path(
        "forgot_password",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("users:forgot_password_sent"),
            extra_email_context={"site_base": settings.SITE_BASE},
        ),
        name="forgot_password",
    ),
    path(
        "forgot_password/sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_sent.html"
        ),
        name="forgot_password_sent",
    ),
    path(
        "forgot_password/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:forgot_password_complete")
        ),
        name="forgot_password_confirm",
    ),
    path(
        "forgot_password/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="forgot_password_complete",
    ),
    path("claim", claim.claim),
    path("set_language", set_language.set_language),
    path("claim/<int:claim_replay_request_id>", claim.review),
    path("my_claims", my_claims.my_claims),
    path("rankings", rankings.rankings),
]
