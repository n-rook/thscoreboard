from typing import Iterable, Optional
from django.shortcuts import redirect, render
from django.contrib.auth import decorators as auth_decorators
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.db import transaction


from users import forms
from users.models import User
from replays import models


@auth_decorators.login_required
def claim(request: WSGIRequest) -> HttpResponse:
    if request.method == "GET":
        return _render_claim_username_form(request)
    elif (
        request.method == "POST" and request.POST.get("royalflare_username") is not None
    ):
        form = forms.ClaimUsernameForm(request.POST)
        if form.is_valid():
            return _render_claim_replay_form(request, form)
        else:
            return _render_claim_username_form(request, form)
    else:
        form = forms.ClaimReplaysForm(request.POST, replays=models.Replay.objects.all())
        if form.is_valid():
            silentselene_username = form.cleaned_data["silentselene_username"]
            user = User.objects.get(username=silentselene_username)
            selected_replay_ids = form.cleaned_data["choices"]
            selected_replays = models.Replay.objects.filter(id__in=selected_replay_ids)
            # _assign_selected_replays_to_user(selected_replays, user)
            return redirect(f"../replays/user/{user}")


def _render_claim_username_form(
    request: WSGIRequest, form: Optional[forms.ClaimUsernameForm] = None
) -> HttpResponse:
    if form is None:
        form = forms.ClaimUsernameForm()
    if not request.user.is_staff:
        form.fields["silentselene_username"].initial = request.user.get_username()
    return render(
        request,
        "replays/claim_username.html",
        {"form": form, "silentselene_username": request.user.get_username()},
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
    request: WSGIRequest, claim_username_form: forms.ClaimUsernameForm
) -> HttpResponse:
    silentselene_username = claim_username_form.cleaned_data["silentselene_username"]
    royalflare_username = claim_username_form.cleaned_data["royalflare_username"]
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
