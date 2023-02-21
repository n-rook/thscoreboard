"""Views related to looking at a saved replay."""

from typing import Iterable, Tuple
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.shortcuts import redirect, render
from django.db import transaction

from replays import models
from replays.lib import http_util
from replays import forms
from replays import game_fields
from replays import reanalyze_replay
from replays import spell_names

from thscoreboard import settings
from replays import game_ids


@http_decorators.require_POST
def edit_replay(request, game_id: str, replay_id: int):
    replay_instance, replay_stages = GetReplayWithStagesOr404(request.user, replay_id)

    edit = forms.EditReplayForm(request.POST)
    if edit.is_valid() and replay_instance.user == request.user:
        replay_instance.comment = edit.cleaned_data['comment']
        replay_instance.save()

    return redirect(replay_details, game_id=game_id, replay_id=replay_id)


@http_decorators.require_safe
def replay_details(request, game_id: str, replay_id: int):
    replay_instance, replay_stages = GetReplayWithStagesOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        # Wrong game, but IDs are unique anyway so we know the right game. Send the user there.
        return redirect(replay_details, game_id=replay_instance.shot.game.game_id, replay_id=replay_id)

    formatStages = game_fields.FormatStages(game_id, replay_stages, replay_instance.shot.GetName())

    edit_form = forms.EditReplayForm(
        initial={
            'comment': replay_instance.comment
        }
    )

    context = {
        'game_name': replay_instance.shot.game.GetName(),
        'shot_name': replay_instance.shot.GetName(),
        'difficulty_name': replay_instance.GetDifficultyName(),
        'game_id': game_id,
        'spell_name': spell_names.get(game_id, replay_instance.spell_card_id),
        'replay': replay_instance,
        'can_edit': request.user == replay_instance.user,
        'can_delete': request.user == replay_instance.user or request.user.is_staff,
        'replay_file_is_good': replay_instance.is_good,
        'has_stages': len(replay_stages) != 0,
        'replay_stages': formatStages,
        'table_fields': game_fields.GetGameField(game_id, replay_instance.replay_type),
        'edit_form': edit_form,
        'replay_type': game_ids.GetReplayType(replay_instance.replay_type),
        'site_base': settings.SITE_BASE
    }

    if hasattr(replay_instance, 'replayfile'):
        context['has_replay_file'] = True
    else:
        context['has_replay_file'] = False

    if replay_instance.route:
        context['route_name'] = replay_instance.route.GetName()

    return render(request, 'replays/replay_details.html', context)


@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
@auth_decorators.permission_required('staff', raise_exception=True)
def view_replay_reanalysis(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    if not replay_instance.shot.game.has_replays:
        raise HttpResponseBadRequest()

    if request.method == 'POST':
        reanalyze_replay.UpdateReplay(replay_id)
        return redirect(replay_details, game_id=replay_instance.shot.game_id, replay_id=replay_id)
    else:
        reanalysis = reanalyze_replay.CheckReplay(replay_id)
        return render(request, 'replays/reanalyze_replay.html', {
            'replay': replay_instance,
            'reanalysis': reanalysis,
        })


@http_decorators.require_safe
def download_replay(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    if not replay_instance.shot.game.has_replays:
        raise HttpResponseBadRequest()

    try:
        replay_file_instance = models.ReplayFile.objects.get(replay=replay_instance)
    except models.ReplayFile.DoesNotExist:
        raise ValueError('No replay file for this submission. This should not be possible')

    download_headers = http_util.GetDownloadFileHeaders(
        ascii_filename=replay_instance.GetNiceFilename(ascii_only=True),
        full_filename=replay_instance.GetNiceFilename(ascii_only=False)
    )

    return HttpResponse(
        replay_file_instance.replay_file,
        headers=download_headers
    )


@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
@auth_decorators.login_required
def delete_replay(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    if not replay_instance.user == request.user and not request.user.is_staff:
        raise HttpResponseForbidden()

    if request.method == 'POST':
        replay_instance.delete()
        return redirect(f'/replays/user/{replay_instance.user.username}')

    return render(
        request,
        'replays/delete_replay.html',
        {
            'game_name': replay_instance.shot.game.GetName(),
            'shot_name': replay_instance.shot.GetName(),
            'difficulty_name': replay_instance.GetDifficultyName(),
            'replay': replay_instance,
        }
    )


def GetReplayOr404(user, replay_id):
    try:
        replay_instance = models.Replay.objects.select_related('shot').visible_to(user).get(id=replay_id)
    except models.Replay.DoesNotExist:
        raise Http404()
    return replay_instance


@transaction.atomic
def GetReplayWithStagesOr404(user, replay_id) -> Tuple[models.Replay, Iterable[models.ReplayStage]]:
    try:
        replay_instance = models.Replay.objects.select_related('shot').visible_to(user).get(id=replay_id)
    except models.Replay.DoesNotExist:
        raise Http404()
    replay_stages = models.ReplayStage.objects.filter(replay=replay_id)
    return replay_instance, replay_stages
