"""The front page of the website."""

from django.shortcuts import render
from django.views.decorators import http as http_decorators

from replays import models
from replays.replays_to_json import (
    convert_replays_to_json_strings,
    stream_json_strings_to_http_reponse,
)


@http_decorators.require_safe
def index_json(request):
    recent_replays = (
        models.Replay.objects.filter(
            category__in=[models.Category.STANDARD, models.Category.TAS]
        )
        .annotate_with_rank()
        .order_by("-created")[:10]
    )
    replay_jsons = convert_replays_to_json_strings(recent_replays)
    return stream_json_strings_to_http_reponse(replay_jsons)


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
