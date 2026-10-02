"""List recent replays."""

from django import shortcuts
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators import http as http_decorators

from replays.views import replay_table_helpers

_NUM_ROWS = 500


@http_decorators.require_safe
def recent_json(request):
    return replay_table_helpers.stream_recent_replays_json(count=_NUM_ROWS)


@http_decorators.require_safe
def recent_replays(
    request: WSGIRequest,
):
    return shortcuts.render(
        request,
        "replays/recent_replays.html",
    )
