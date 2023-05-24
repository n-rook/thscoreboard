from typing import Iterable, Optional, Tuple
from django.shortcuts import redirect, render
from django.contrib.auth import decorators as auth_decorators
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponse
from django.db import transaction
from django.core.exceptions import PermissionDenied


from users import forms
import users.models as user_models
import replays.models as replay_models


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
        form = forms.ClaimReplaysForm(
            request.POST, replays=replay_models.Replay.objects.all()
        )
        if form.is_valid():
            replays, user = _get_replays_and_user_from_form(form)
            _submit_claim(
                replays,
                user,
                is_request_from_staff=request.user.is_staff,
                contact_info=form.cleaned_data["contact_info"],
            )
            if request.user.is_staff:
                return render(request, "replays/success.html")
            return redirect("/users/my_claims")


@auth_decorators.login_required
def review(request: WSGIRequest, claim_replay_request_id: int) -> HttpResponse:
    claim: user_models.ClaimReplayRequest = (
        user_models.ClaimReplayRequest.objects.filter(
            id=claim_replay_request_id
        ).first()
    )
    if claim is None:
        raise Http404
    if not _check_user_can_see_claim(request.user, claim):
        raise PermissionDenied

    if request.method == "POST":
        form = forms.ClaimReplaysForm(
            request.POST, replays=replay_models.Replay.objects.all()
        )
        if form.is_valid():
            submit_action = form.cleaned_data["submit_action"]
            replays, user = _get_replays_and_user_from_form(form)
            if submit_action == forms.ClaimReplaysForm.SUBMIT_ACTIONS.APPROVE:
                _assign_selected_replays_to_user(replays, user, claim)
                return render(request, "replays/success.html")
            elif submit_action == forms.ClaimReplaysForm.SUBMIT_ACTIONS.DELETE:
                _delete_claim_replay_request(claim, request.user.is_staff)
                return render(request, "replays/success.html")
            else:
                raise ValueError(f"Unknown submit value: {submit_action}")
        else:
            return _render_review_form(request, claim, form)
    else:
        return _render_review_form(request, claim)


def _render_review_form(
    request: WSGIRequest,
    claim: user_models.ClaimReplayRequest,
    form: forms.ClaimReplaysForm = None,
) -> HttpResponse:
    replays = claim.replays.all()
    if form is None:
        form = forms.ClaimReplaysForm(replays=replays)
    form.fields["contact_info"].initial = claim.contact_info
    form.fields["contact_info"].widget.attrs["readonly"] = "readonly"
    return render(
        request,
        "replays/claim_replays.html",
        {
            "form": form,
            "replays": replays,
            "silentselene_username": claim.user.username,
            "is_review": True,
        },
    )


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


def _submit_claim(
    replays: Iterable[replay_models.Replay],
    user: user_models.User,
    is_request_from_staff: bool,
    contact_info: str,
) -> None:
    if is_request_from_staff:
        _assign_selected_replays_to_user(replays, user)
    else:
        _create_new_claim_replay_request(replays, user, contact_info)


def _create_new_claim_replay_request(
    replays: Iterable[replay_models.Replay],
    user: user_models.User,
    contact_info: str,
) -> None:
    claim_replay_request = user_models.ClaimReplayRequest.objects.create(
        user=user,
        contact_info=contact_info,
        request_status=user_models.RequestStatus.SUBMITTED,
    )
    claim_replay_request.save()
    claim_replay_request.replays.set(replays)


@transaction.atomic
def _assign_selected_replays_to_user(
    replays: Iterable[replay_models.Replay],
    user: user_models.User,
    claim: Optional[user_models.ClaimReplayRequest] = None,
) -> None:
    for replay in replays:
        if replay.user is None:
            replay.user = user
            replay.save()
        else:
            if replay.user != user:
                raise ValueError("Replay already belongs to a different user.")
    if claim is not None:
        claim.request_status = user_models.RequestStatus.APPROVED
        claim.save()


def _delete_claim_replay_request(
    claim: user_models.ClaimReplayRequest, is_staff: bool
) -> None:
    if is_staff:
        claim.request_status = user_models.RequestStatus.STAFF_DELETED
    else:
        claim.request_status = user_models.RequestStatus.USER_DELETED
    claim.save()


def _render_claim_replay_form(
    request: WSGIRequest, claim_username_form: forms.ClaimUsernameForm
) -> HttpResponse:
    silentselene_username = claim_username_form.cleaned_data["silentselene_username"]
    royalflare_username = claim_username_form.cleaned_data["royalflare_username"]
    replays = _get_unclaimed_replays_from_username(royalflare_username)
    form = forms.ClaimReplaysForm(replays=replays)
    if request.user.is_staff:
        form.fields["contact_info"].initial = "Not applicable"
        form.fields["contact_info"].widget.attrs["readonly"] = "readonly"
    return render(
        request,
        "replays/claim_replays.html",
        {
            "form": form,
            "replays": replays,
            "silentselene_username": silentselene_username,
            "is_review": False,
        },
    )


def _get_replays_and_user_from_form(
    form: forms.ClaimReplaysForm,
) -> Tuple[Iterable[replay_models.Replay], user_models.User]:
    silentselene_username = form.cleaned_data["silentselene_username"]
    user = user_models.User.objects.get(username=silentselene_username)
    selected_replay_ids = form.cleaned_data["choices"]
    selected_replays = replay_models.Replay.objects.filter(
        id__in=selected_replay_ids
    ).all()
    return selected_replays, user


def _get_unclaimed_replays_from_username(
    username: str,
) -> Iterable[replay_models.Replay]:
    return (
        replay_models.Replay.objects.filter(imported_username__iexact=username)
        .filter(user__isnull=True)
        .all()
    )


def _check_user_can_see_claim(
    user: user_models.User, claim: user_models.ClaimReplayRequest
) -> bool:
    if user.is_staff:
        return True
    if (
        user == claim.user
        and claim.request_status == user_models.RequestStatus.SUBMITTED
    ):
        return True
    return False
