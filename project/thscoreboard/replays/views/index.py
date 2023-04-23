"""The front page of the website."""

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators import http as http_decorators

from replays import models
from replays.replays_to_json import (
    ReplayToJsonConverter,
    add_rank_annotation_to_replays,
)


@http_decorators.require_safe
def index_json(request):
    not_unusual_replays = models.Replay.objects.filter(
        category__in=[models.Category.REGULAR, models.Category.TAS]
    )
    ranked_not_unusual_replays = add_rank_annotation_to_replays(not_unusual_replays)
    recent_replays = ranked_not_unusual_replays.order_by("-created")[:10]
    converter = ReplayToJsonConverter()
    return JsonResponse(
        converter.convert_replays_to_serializable_list(recent_replays), safe=False
    )


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
