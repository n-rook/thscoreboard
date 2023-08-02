"""The public page for a user's information."""


from django.contrib import auth
from django.shortcuts import get_object_or_404, render
from django.views.decorators import http as http_decorators

from replays import models
from replays.replays_to_json import convert_replays_to_json_bytes
from replays.views.replay_table_helpers import stream_json_bytes_to_http_reponse


@http_decorators.require_safe
def user_page_json(request, username: str):
    user = get_object_or_404(auth.get_user_model(), username=username, is_active=True)
    user_replays = models.Replay.objects.filter(user=user).order_by(
        "shot__game_id", "shot_id", "created"
    )

    top_3_replays = (
        models.Replay.objects.filter(category=models.Category.STANDARD)
        .filter(replay_type=1)
        .filter(is_listed=True)
        .annotate_with_rank()
        .filter(rank__lte=3)
        .all()
    )
    rank_dict = {replay.id: replay.rank for replay in top_3_replays}

    for replay in user_replays:
        replay.rank = rank_dict.get(replay.id, -1)
    replay_jsons = convert_replays_to_json_bytes(user_replays)
    return stream_json_bytes_to_http_reponse(replay_jsons)


@http_decorators.require_safe
def user_page(request, username: str):
    user = get_object_or_404(auth.get_user_model(), username=username, is_active=True)
    is_own_page = user == request.user

    return render(
        request,
        "replays/user_page.html",
        {"viewed_user": user, "is_own_page": is_own_page},
    )
