"""Contains views which list various replays."""

from django.http import JsonResponse
from django.views.decorators import http as http_decorators
from django.shortcuts import get_object_or_404, render

from replays import models
from replays.models import Game, Shot
from replays.replays_to_json import ReplayToJsonConverter


@http_decorators.require_safe
def game_scoreboard_json(request, game_id: str):
    converter = ReplayToJsonConverter()
    return JsonResponse(
        converter.convert_replays_to_serializable_list(
            _get_all_replay_for_game(game_id)
        ),
        safe=False,
    )


@http_decorators.require_safe
def game_scoreboard(request, game_id: str):
    game: Game = get_object_or_404(Game, game_id=game_id)
    all_shots = [shot.GetName() for shot in Shot.objects.filter(game=game_id)]
    all_difficulties = [game.GetDifficultyName(d) for d in range(game.num_difficulties)]

    return render(
        request,
        "replays/game_scoreboard.html",
        {"game": game, "shots": all_shots, "difficulties": all_difficulties},
    )


def _get_all_replay_for_game(game_id: str) -> dict:
    return (
        models.Replay.objects.select_related("shot")
        .filter(category=models.Category.REGULAR)
        .filter(shot__game=game_id)
        .filter(replay_type=1)
        .order_by("-score")
    )
