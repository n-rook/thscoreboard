"""This module contains information related to banned users."""

from django.contrib.auth import decorators as auth_decorators
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators import http as http_decorators

from users import forms
from users import models
from users.middleware import check_ban


@auth_decorators.login_required
@http_decorators.require_safe
@check_ban.allow_access_by_banned_users
def banned_notification(request):
    """Inform the user why they are banned."""

    with transaction.atomic():
        if not request.user.CheckIfBanned():
            # The user is not banned, just send them to the homepage.
            return redirect("/")

        latest_ban = models.Ban.objects.filter(target=request.user).order_by(
            "-expiration"
        )[0]

    return render(
        request,
        "users/banned.html",
        {
            "reason": latest_ban.reason,
            "expiration": latest_ban.expiration,
        },
    )


@auth_decorators.login_required
@auth_decorators.permission_required("staff", raise_exception=True)
def staff_ban(request):
    """A page where staff can temporarily ban other users."""
    if request.method == "POST":
        form = forms.BanForm(request.POST)
        if form.is_valid():
            form.cleaned_data["target"].BanUser(
                author=request.user,
                reason=form.cleaned_data["reason"],
                duration=form.GetDuration(),
            )

            return render(
                request,
                "users/ban_success.html",
                {"target": form.cleaned_data["target"]},
            )

        # If the form is not valid, fall through to the GET page, and render it that way.
    else:
        form = forms.BanForm()

    return render(request, "users/ban_form.html", {"form": form})
