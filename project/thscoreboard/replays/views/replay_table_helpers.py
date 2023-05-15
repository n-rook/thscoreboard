from typing import Iterable
from django.http import StreamingHttpResponse


def stream_json_bytes_to_http_reponse(
    replay_bytes: Iterable[bytes],
) -> StreamingHttpResponse:
    response = StreamingHttpResponse(
        iter(replay_bytes),
        content_type="application/json",
    )
    response["Content-Disposition"] = 'attachment; filename="output.json"'
    return response
