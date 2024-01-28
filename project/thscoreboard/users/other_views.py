"""Defines views for user and account management."""

# TODO: Separate views in different files and put in views/.

from django.http import HttpResponseBadRequest

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators

from . import forms
from . import models


@auth_decorators.login_required
@auth_decorators.permission_required("staff", raise_exception=True)
@http_decorators.require_http_methods(["GET", "HEAD"])
def view_ip_bans(request):
    return render(
        request,
        "users/ip_bans.html",
        {
            "ip_bans": models.IPBan.objects.all(),
            "add_ip_ban_form": forms.AddIPBanForm(),
        },
    )


@auth_decorators.login_required
@auth_decorators.permission_required("staff", raise_exception=True)
@http_decorators.require_http_methods(["GET", "HEAD"])
def delete_ip_ban(request, ban_id: int):
    models.IPBan.objects.get(id=ban_id).delete()
    return redirect("/users/ip_bans")


@auth_decorators.login_required
@auth_decorators.permission_required("staff", raise_exception=True)
@http_decorators.require_POST
def add_ip_ban(request):
    form = forms.AddIPBanForm(request.POST)
    if form.is_valid():
        try:
            models.validate_ip(form.cleaned_data["ip"])
        except ValidationError as e:
            return HttpResponseBadRequest(content=e)
        models.IPBan(
            ip=form.cleaned_data["ip"],
            comment=form.cleaned_data["comment"],
            author=request.user,
        ).save()
    return redirect("/users/ip_bans")
