"""The front page of the website."""

from django.shortcuts import render
from django.views.decorators import http as http_decorators

from replays import models
from replays.views import replay_table_helpers


@http_decorators.require_safe
def index_json(request):
    return replay_table_helpers.stream_recent_replays_json(count=20)


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
