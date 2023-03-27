"""Contains views for players accepting invites to the site."""

from django.http import Http404

from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.decorators import http as http_decorators

from users import forms
from users import models


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def accept_invite(request, token: str):
    try:
        invited_user = models.InvitedUser.objects.get(token=token)
    except models.InvitedUser.DoesNotExist:
        raise Http404("We could not find your invite.")

    if request.method == "POST":
        form = forms.AcceptInviteForm(request.POST)
        if form.is_valid():
            new_acct = invited_user.AcceptInvite(form.cleaned_data["password"])
            auth.login(request, new_acct)
            return redirect("users:registration_success")
    else:
        form = forms.AcceptInviteForm(
            initial={
                "username": invited_user.username,
                "email": invited_user.email,
            }
        )

    return render(
        request,
        "users/accept_invite.html",
        {
            "form": form,
            "invited_user": invited_user,
        },
    )
