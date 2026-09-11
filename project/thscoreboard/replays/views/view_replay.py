"""Views related to looking at a saved replay."""

from typing import Iterable, Tuple
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    Http404,
)
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.shortcuts import redirect, render
from django.db import transaction
from django.utils.translation import gettext as _

from replays import models
from replays.lib import http_util
from replays.lib.video_embed import get_video_embed_link
from replays import forms
from replays import game_fields
from replays import reanalyze_replay
from replays import spell_names

from thscoreboard import settings
from replays import game_ids


@http_decorators.require_POST
def edit_comment(request, game_id: str, replay_id: int):
    replay_instance, replay_stages = GetReplayWithStagesOr404(request.user, replay_id)

    edit = forms.EditReplayForm(request.POST)
    if edit.is_valid() and replay_instance.user == request.user:
        replay_instance.comment = edit.cleaned_data["comment"]
        replay_instance.save()

    return redirect(replay_details, game_id=game_id, replay_id=replay_id)


@http_decorators.require_safe
def replay_details(request, game_id: str, replay_id: int):
    replay_instance, replay_stages = GetReplayWithStagesOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        # Wrong game, but IDs are unique anyway so we know the right game. Send the user there.
        return redirect(
            replay_details,
            game_id=replay_instance.shot.game.game_id,
            replay_id=replay_id,
        )

    formatStages = game_fields.FormatStages(
        game_id, replay_stages, replay_instance.shot.shot_id
    )

    th03_stage = replay_stages.first() if game_id == game_ids.GameIDs.TH03 else None

    edit_form = forms.EditReplayForm(initial={"comment": replay_instance.comment})

    can_remove_claim = _is_replay_claimed(replay_instance) and (
        request.user == replay_instance.user or request.user.is_staff
    )

    context = {
        "game_name": replay_instance.shot.game.GetName(),
        "shot_name": replay_instance.shot.GetName(),
        "difficulty_name": replay_instance.GetDifficultyDisplayName(),
        "category": replay_instance.get_category_display(),
        "game_id": game_id,
        "spell_name": spell_names.get(
            game_id,
            replay_instance.spell_card_id,
            replay_instance.scene_game_level,
            replay_instance.scene_game_scene,
        ),
        "replay": replay_instance,
        "can_edit": request.user == replay_instance.user,
        "can_delete": request.user == replay_instance.user or request.user.is_staff,
        "is_listed": replay_instance.is_listed,
        "replay_file_is_good": replay_instance.is_good,
        "has_stages": len(replay_stages) != 0,
        "replay_stages": formatStages,
        "table_fields": game_fields.GetGameField(game_id, replay_instance.replay_type),
        "edit_form": edit_form,
        "replay_type": game_ids.GetReplayType(replay_instance.replay_type),
        "site_base": settings.SITE_BASE,
        "can_remove_claim": can_remove_claim,
        "show_th03_cpu": (
            th03_stage is not None
            and (
                th03_stage.th03_player_cpu is not None
                or th03_stage.th03_opponent_cpu is not None
            )
        ),
        "th03_player_cpu": th03_stage.th03_player_cpu if th03_stage else None,
        "th03_opponent_cpu": th03_stage.th03_opponent_cpu if th03_stage else None,
        "th03_ruleset_name": (
            (_("Stock"), _("Dopamine Arrange"))[replay_instance.th03_ruleset]
            if replay_instance.th03_ruleset in (0, 1)
            else None
        ),
        "show_th03_netplay": (
            game_id == game_ids.GameIDs.TH03
            and replay_instance.replay_type == game_ids.ReplayTypes.PVP
        ),
    }

    if hasattr(replay_instance, "replayfile"):
        context["has_replay_file"] = True
    else:
        context["has_replay_file"] = False
    if replay_instance.user:
        context["player_name"] = replay_instance.user.username
        context["owned"] = True
    else:
        context["player_name"] = replay_instance.imported_username
        context["owned"] = False

    if replay_instance.route:
        context["route_name"] = replay_instance.route.GetName()

    if replay_instance.video_link:
        context["video_embed"] = get_video_embed_link(replay_instance.video_link)

    return render(request, "replays/replay_details.html", context)


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
@auth_decorators.permission_required("staff", raise_exception=True)
def view_replay_reanalysis(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    if not hasattr(replay_instance, "replayfile"):
        return HttpResponseBadRequest()

    if request.method == "POST":
        reanalyze_replay.UpdateReplay(replay_id)
        return redirect(
            replay_details, game_id=replay_instance.shot.game_id, replay_id=replay_id
        )
    else:
        reanalysis = reanalyze_replay.CheckReplay(replay_id)
        return render(
            request,
            "replays/reanalyze_replay.html",
            {
                "replay": replay_instance,
                "reanalysis": reanalysis,
            },
        )


@http_decorators.require_safe
def download_replay(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    try:
        replay_file_instance = models.ReplayFile.objects.get(replay=replay_instance)
    except models.ReplayFile.DoesNotExist:
        raise Http404()

    download_headers = http_util.GetDownloadFileHeaders(
        replay_instance.GetNiceFilename(replay_file_instance.id)
    )

    return HttpResponse(replay_file_instance.replay_file, headers=download_headers)


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
@auth_decorators.login_required
def delete_replay(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    if not replay_instance.user == request.user and not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == "POST":
        replay_instance.delete()
        return redirect(f"/replays/user/{replay_instance.user.username}")

    return render(
        request,
        "replays/delete_replay.html",
        {
            "game_name": replay_instance.shot.game.GetName(),
            "shot_name": replay_instance.shot.GetName(),
            "difficulty_name": replay_instance.GetDifficultyDisplayName(),
            "replay": replay_instance,
        },
    )


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
@auth_decorators.login_required
def unclaim_replay(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)
    if not _is_replay_claimed(replay_instance):
        return HttpResponseBadRequest()
    if not replay_instance.user == request.user and not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == "POST":
        replay_instance.user = None
        replay_instance.save()
        return redirect(f"/replays/{game_id}/{replay_id}")

    return render(
        request,
        "replays/unclaim_replay.html",
        {
            "game_name": replay_instance.shot.game.GetName(),
            "shot_name": replay_instance.shot.GetName(),
            "difficulty_name": replay_instance.GetDifficultyDisplayName(),
            "replay": replay_instance,
        },
    )


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
@auth_decorators.login_required
def list_replay(request, game_id: str, replay_id: int):
    _set_listed(request, game_id, replay_id, True)
    return replay_details(request, game_id, replay_id)


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
@auth_decorators.login_required
def unlist_replay(request, game_id: str, replay_id: int):
    _set_listed(request, game_id, replay_id, False)
    return replay_details(request, game_id, replay_id)


def _set_listed(request, game_id: str, replay_id: int, listed) -> None:
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    if not replay_instance.user == request.user and not request.user.is_staff:
        raise HttpResponseForbidden()

    replay_instance.is_listed = listed
    replay_instance.save()


def GetReplayOr404(user, replay_id):
    try:
        replay_instance = (
            models.Replay.objects.select_related("shot")
            .filter_visible()
            .get(id=replay_id)
        )
    except models.Replay.DoesNotExist:
        raise Http404()
    return replay_instance


@transaction.atomic
def GetReplayWithStagesOr404(
    user, replay_id
) -> Tuple[models.Replay, Iterable[models.ReplayStage]]:
    try:
        replay_instance = (
            models.Replay.objects.select_related("shot")
            .filter_visible()
            .get(id=replay_id)
        )
    except models.Replay.DoesNotExist:
        raise Http404()
    replay_stages = models.ReplayStage.objects.filter(replay=replay_id)
    return replay_instance, replay_stages


def _is_replay_claimed(replay: models.Replay) -> bool:
    return replay.imported_username is not None and replay.user is not None
