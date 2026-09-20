"""The front page of the website."""

from django.shortcuts import render
from django.views.decorators import http as http_decorators

from replays.views.replay_table_helpers import stream_json_bytes_to_http_reponse
from replays import models
from replays.replays_to_json import convert_replays_to_json_bytes
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
