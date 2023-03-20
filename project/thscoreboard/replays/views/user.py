"""The public page for a user's information."""


from django.contrib import auth
from django.shortcuts import get_object_or_404, render
from django.views.decorators import http as http_decorators

from replays import models
from replays.replays_to_json import convert_replays_to_json_string


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def user_page(request, username: str):
    user = get_object_or_404(auth.get_user_model(), username=username, is_active=True)

    user_replays = (
        models.Replay.objects.visible_to(request.user)
        .filter(user=user)
        .order_by("shot__game_id", "shot_id", "created")
    )
    replays_json = convert_replays_to_json_string(user_replays)

    return render(
        request,
        "replays/user_page.html",
        {
            "viewed_user": user,
            "replaysJSON": replays_json,
        },
    )
