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
        return _render_claim_replay_form(request)
    else:
        form = forms.ClaimReplaysForm(request.POST)
        if form.is_valid():
            print("FORM", form)
            print("FORM", form.cleaned_data)
            selected_replays = form.cleaned_data["replays"]
            print(selected_replays)
            # Do something with selected_replays
        selected_replays = _get_selected_replays(request)
        user = _get_user(request.POST["silentselene_username"])
        # _assign_selected_replays_to_user(selected_replays, user)
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


def _get_selected_replays(request: WSGIRequest) -> list[models.Replay]:
    selected_replays = []
    for replay_id, checkbox_value in request.POST.items():
        replay_was_selected = checkbox_value == "on"
        if replay_was_selected:
            replay = models.Replay.objects.get(id=replay_id)
            selected_replays.append(replay)
    return selected_replays


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


def _render_claim_replay_form(request: WSGIRequest) -> HttpResponse:
    silentselene_username = request.POST.get("silentselene_username")
    _assert_username_is_valid(request.POST.get("silentselene_username"))
    royalflare_username = request.POST.get("royalflare_username")
    replays = _get_unclaimed_replays_from_username(royalflare_username)
    form = forms.ClaimReplaysForm(replays=replays)
    replays_with_inputs = zip(replays, form.confirm_replay_inputs)
    return render(
        request,
        "replays/claim_replays.html",
        {
            "replays_with_inputs": replays_with_inputs,
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


def _assert_username_is_valid(username: str) -> User:
    _get_user(username)
