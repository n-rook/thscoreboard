"""The front page of the website."""

from django.shortcuts import render
from django.views.decorators import http as http_decorators

from replays.views.replay_table_helpers import stream_json_bytes_to_http_reponse
from replays import models
from replays.replays_to_json import convert_replays_to_json_bytes


@http_decorators.require_safe
def index_json(request):
    recent_replays = (
        models.Replay.objects.filter(
            category__in=[models.Category.STANDARD, models.Category.TAS]
        )
        .filter(is_listed=True)
        .annotate_with_rank()
        .order_by("-created")[:10]
    )
    replay_jsons = convert_replays_to_json_bytes(recent_replays)
    return stream_json_bytes_to_http_reponse(replay_jsons)


@http_decorators.require_safe
def index(request):
    all_games = models.Game.objects.all()

    return render(
        request,
        "replays/index.html",
        {
            "all_games": all_games,
        },
    )
