"""The front page of the website."""

from django.shortcuts import render
from django.views.decorators import http as http_decorators

from replays import models
from replays.views.replay_list import convert_replays_to_json_string


@http_decorators.require_safe
def index(request):
    all_games = models.Game.objects.all()

    recent_uploads = (
        models.Replay.objects
        .filter_visible()
        .filter(category__in=[models.Category.REGULAR, models.Category.TAS])
        .order_by('-created')
        [:10]
    )
    
    recent_replays = (
        models.Replay.objects
        .visible_to(request.user)
        .filter(category__in=[models.Category.REGULAR, models.Category.TAS])
        .order_by('-created')
        [:10]
    )
    replays_json = convert_replays_to_json_string(recent_replays)

    return render(
        request, 'replays/index.html',
        {
            'all_games': all_games,
            'recent_uploads': recent_uploads,
            'replaysJSON': replays_json,
        })
