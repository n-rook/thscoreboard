from typing import Iterable
from django.http import StreamingHttpResponse

from replays import models
from replays.replays_to_json import convert_replays_to_json_bytes


def stream_json_bytes_to_http_response(
    replay_bytes: Iterable[bytes],
) -> StreamingHttpResponse:
    response = StreamingHttpResponse(
        iter(replay_bytes),
        content_type="application/json",
    )
    response["Content-Disposition"] = 'attachment; filename="output.json"'
    return response


def stream_recent_replays_json(count: int) -> StreamingHttpResponse:
    """Fetch recent replays and stream them as JSON."""

    recent_replays = (
        models.Replay.objects.select_related("rank_view")
        .filter(category__in=[models.Category.STANDARD, models.Category.TAS])
        .filter(is_listed=True)
        .filter_visible()
        .order_by("-created")[:count]
    )
    replay_jsons = convert_replays_to_json_bytes(recent_replays)
    return stream_json_bytes_to_http_response(replay_jsons)
