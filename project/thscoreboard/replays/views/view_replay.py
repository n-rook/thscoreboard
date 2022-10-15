"""Views related to looking at a saved replay."""

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.shortcuts import redirect, render

from replays import models
from replays.lib import http_util


@http_decorators.require_safe
def replay_details(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        # Wrong game, but IDs are unique anyway so we know the right game. Send the user there.
        return redirect(replay_details, game_id=replay_instance.shot.game.game_id, replay_id=replay_id)

    context = {
        'game_name': replay_instance.shot.game.GetName(),
        'shot_name': replay_instance.shot.GetName(),
        'difficulty_name': replay_instance.GetDifficultyName(),
        'game_id': game_id,
        'replay': replay_instance,
        'is_owner': request.user == replay_instance.user,
        'replay_file_is_good': replay_instance.is_good
    }
    if hasattr(replay_instance, 'replayfile'):
        context['has_replay_file'] = True
    else:
        context['has_replay_file'] = False

    if replay_instance.route:
        context['route_name'] = replay_instance.route.GetName()

    return render(request, 'replays/replay_details.html', context)


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
    if not replay_instance.user == request.user:
        raise HttpResponseForbidden()
    
    if request.method == 'POST':
        replay_instance.delete()
        return redirect(f'/replays/user/{request.user.username}')
    
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
        replay_instance = models.Replay.objects.select_related('shot').get(id=replay_id)
    except models.Replay.DoesNotExist:
        raise Http404()
    if not replay_instance.IsVisible(user):
        raise Http404()
    return replay_instance
