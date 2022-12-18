"""Middleware that records the IP addresses of users in the database."""

from concurrent import futures
import logging
from typing import Optional

from django.http import request as request_lib

from users import models


_MAX_WORKERS = 100


def _get_ip(request: request_lib.HttpRequest) -> Optional[str]:
    return request.META.get('REMOTE_ADDR')


class RecordIPMiddleware:
    """Middleware that records the IP addresses of incoming requests."""

    def __init__(self, get_response) -> None:
        self._get_response = get_response

        self._executor = futures.ThreadPoolExecutor(
            max_workers=_MAX_WORKERS,
            thread_name_prefix='RecordIPMiddleware')

    def __call__(self, request: request_lib.HttpRequest):
        ip = _get_ip(request)

        # To save time and lower the chances of delaying a response, we save the
        # IP address in parallel with returning a response.
        save_ip_future = self._executor.submit(self._SaveIP, ip, request.user)
        response = self._get_response(request)
        save_ip_future.result(timeout=60)
        return response

    def _SaveIP(self, ip: str, user: models.User):
        if not ip:
            logging.warning('No IP detected for this request; this should not happen')
            return

        if user.is_anonymous:
            models.Visits.RecordVisit(None, ip)
        else:
            models.Visits.RecordVisit(user, ip)
