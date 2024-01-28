"""Views related to editing an existing replay."""

from django import urls
from django import shortcuts
from django.template import response as template_response
from django import http
from django.utils.translation import gettext as _
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators

from replays import forms
from replays import models


@auth_decorators.login_required
@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def edit_replay(request: http.HttpRequest, game_id: str, replay_id: int):
    """Edit an existing replay."""

    try:
        replay = models.Replay.objects.get(id=replay_id)
    except models.Replay.DoesNotExist:
        raise http.Http404()

    if request.user != replay.user:
        return shortcuts.render(
            request,
            "replays/edit_replay_not_allowed.html",
            context={"game_id": game_id, "replay_id": replay_id},
            status=403,
        )

    if not hasattr(replay, "replayfile"):
        return shortcuts.render(
            request,
            "simple_message.html",
            context={
                "message": _("We do not yet support editing PC-98 replays."),
            },
        )

    game = replay.shot.game

    if request.method == "POST":
        form = forms.initialize_publish_replay_form_from_replay(
            replay, data=request.POST
        )
        if form.is_valid():
            form.update_replay(replay)
            replay.save()
            return shortcuts.redirect(
                urls.reverse("Replays/Details", args=[game_id, replay_id])
            )
    else:
        form = forms.initialize_publish_replay_form_from_replay(replay)

    context = {
        "form": form,
        "game_name": game.GetName(),
        "game_id": game.game_id,
        "difficulty_name": replay.GetDifficultyName(),
        "shot_name": replay.shot.GetName(),
        "has_replay_file": True,
        "replay_type": replay.GetReplayTypeName(),
    }
    if replay.timestamp:
        context["replay_timestamp"] = replay.timestamp
    if replay.slowdown is not None:
        context["replay_slowdown"] = replay.slowdown
    if replay.spell_card_id:
        context["replay_spell_card_id"] = replay.spell_card_id_format
    if replay.route:
        context["route_name"] = replay.route.GetName()

    return template_response.TemplateResponse(
        request, "replays/edit_replay.html", context
    )
