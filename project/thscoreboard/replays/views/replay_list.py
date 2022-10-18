"""Contains views which list various replays."""

from typing import Optional

from django.http import Http404
from django.views.decorators import http as http_decorators
from django.shortcuts import get_object_or_404, render

from replays import game_ids
from replays import models


@http_decorators.require_safe
def game_scoreboard(request, game_id: str, difficulty: Optional[int] = None, shot_id: Optional[str] = None):
    # Ancient wisdom: You don't need pagination if you don't have users yet!
    game = get_object_or_404(models.Game, game_id=game_id)
    all_replays = (
        models.Replay.objects.select_related('shot', 'replayfile')
        .filter(category=models.Category.REGULAR)
        .filter(shot__game=game_id)
        .order_by('-score')
    )
    extra_params = {}
    if difficulty is not None:
        if difficulty < 0 or difficulty >= game.num_difficulties:
            raise Http404()
        all_replays = all_replays.filter(difficulty=difficulty)
        extra_params['difficulty'] = difficulty
        extra_params['difficulty_name'] = game_ids.GetDifficultyName(game.game_id, difficulty)

    if shot_id is not None:
        shot = get_object_or_404(models.Shot, game=game_id, shot_id=shot_id)
        all_replays = all_replays.filter(shot=shot)
        extra_params['shot'] = shot

    return render(
        request,
        'replays/game_scoreboard.html',
        {
            'game': game,
            'replays': all_replays,
            **extra_params
        })
