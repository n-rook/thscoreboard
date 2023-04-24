"""The front page of the website."""

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators import http as http_decorators

from replays import models
from replays.replays_to_json import ReplayToJsonConverter


@http_decorators.require_safe
def index_json(request):
    recent_replays = (
        models.Replay.objects.filter(
            category__in=[models.Category.REGULAR, models.Category.TAS]
        )
        .annotate_with_rank()
        .order_by("-created")[:10]
    )
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
