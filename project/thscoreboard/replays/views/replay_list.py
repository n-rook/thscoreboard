"""Contains views which list various replays."""

from multiprocessing.managers import BaseManager
from typing import Iterable, Optional

from django.http import Http404
from django.views.decorators import http as http_decorators
from django.shortcuts import get_object_or_404, render

from replays import game_ids
from replays import models
from replays.models import Game, Shot


@http_decorators.require_safe
def game_scoreboard(request, game_id: str, difficulty: Optional[int] = None, shot_id: Optional[str] = None):
    # Ancient wisdom: You don't need pagination if you don't have users yet!
    game: Game = get_object_or_404(Game, game_id=game_id)
    all_shots: Iterable[Shot] = Shot.objects.filter(game=game_id)
    all_difficulties: list[int] = list(range(game.num_difficulties))
    difficulty_names = [game.GetDifficultyName(d) for d in all_difficulties]

    print([shot.GetName() for shot in all_shots])
    print([d for d in all_difficulties])

    all_replays = (
        models.Replay.objects.select_related('shot')
        .filter_visible()
        .filter(category=models.Category.REGULAR)
        .filter(shot__game=game_id)
        .filter(replay_type=1)
        .order_by('-score')
    )
    extra_params = {}
    # if difficulty is not None:
    #     if difficulty < 0 or difficulty >= game.num_difficulties:
    #         raise Http404()
    #     all_replays = all_replays.filter(difficulty=difficulty)
    #     extra_params['difficulty'] = difficulty
    #     extra_params['difficulty_name'] = game_ids.GetDifficultyName(game.game_id, difficulty)

    # if shot_id is not None:
    #     shot = get_object_or_404(models.Shot, game=game_id, shot_id=shot_id)
    #     all_replays = all_replays.filter(shot=shot)
    #     extra_params['shot'] = shot

    return render(
        request,
        'replays/game_scoreboard.html',
        {
            'game': game,
            'shots': all_shots,
            'difficulties': difficulty_names,
            'replays': all_replays,
            **extra_params
        })
