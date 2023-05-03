"""The front page of the website."""

from typing import Iterable
from django.shortcuts import redirect, render
from django.contrib.auth import decorators as auth_decorators
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.db import transaction


from users import forms
from users.models import User
from replays import models


# @auth_decorators.login_required
# @auth_decorators.permission_required("staff", raise_exception=True)
def claim(request: WSGIRequest) -> HttpResponse:
    if request.method == "GET":
        return _render_claim_username_form(request)
    elif (
        request.method == "POST" and request.POST.get("royalflare_username") is not None
    ):
        form = forms.ClaimUsernameForm(request.POST)
        if form.is_valid():
            return _render_claim_replay_form(form, request)
    else:
        form = forms.ClaimReplaysForm(request.POST, replays=models.Replay.objects.all())
        if form.is_valid():
            silentselene_username = form.cleaned_data["silentselene_username"]
            user = _get_user(silentselene_username)
            selected_replay_ids = form.cleaned_data["choices"]
            selected_replays = models.Replay.objects.filter(id__in=selected_replay_ids)
            _assign_selected_replays_to_user(selected_replays, user)
            return redirect(f"../replays/user/{user}")


def _render_claim_username_form(request: WSGIRequest) -> HttpResponse:
    form = forms.ClaimUsernameForm()
    return render(
        request,
        "replays/claim_username.html",
        {
            "form": form,
        },
    )


@transaction.atomic
def _assign_selected_replays_to_user(
    replays: Iterable[models.Replay], user: User
) -> None:
    for replay in replays:
        if replay.user is None:
            replay.user = user
            replay.save()
        else:
            if replay.user != user:
                raise ValueError("Replay already belongs to a different user.")


def _render_claim_replay_form(
    claim_username_form: forms.ClaimUsernameForm, request: WSGIRequest
) -> HttpResponse:
    silentselene_username = claim_username_form.cleaned_data["silentselene_username"]
    royalflare_username = claim_username_form.cleaned_data["royalflare_username"]
    if not are_usernames_valid(
        royalflare_username=royalflare_username,
        silentselene_username=silentselene_username,
    ):
        pass
        # TODO handle errors
    replays = _get_unclaimed_replays_from_username(royalflare_username)
    claim_replays_form = forms.ClaimReplaysForm(replays=replays)
    return render(
        request,
        "replays/claim_replays.html",
        {
            "form": claim_replays_form,
            "replays": replays,
            "silentselene_username": silentselene_username,
        },
    )


def _get_unclaimed_replays_from_username(username: str) -> Iterable[models.Replay]:
    return (
        models.Replay.objects.filter(imported_username__iexact=username)
        .filter(user__isnull=True)
        .all()
    )


def _get_user(username: str) -> User:
    return User.objects.get(username=username)


def are_usernames_valid(royalflare_username: str, silentselene_username: str) -> User:
    pass
    # TODO
