"""Middleware that redirects banned users to a specific location."""

import functools

from django.http import request as request_lib
from django.shortcuts import redirect


def allow_access_by_banned_users(view_func):
    """Mark a view as being accessible by banned accounts.

    This decorator is heavily inspired by the csrf_exempt decorator built into
    Django.
    """

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapper.ban_ok = True
    return wrapper


class CheckBanMiddleware:
    """Middleware that records the IP addresses of incoming requests."""

    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request: request_lib.HttpRequest):
        """Just call the next function; this middleware doesn't do anything here."""

        return self._get_response(request)

    def _CheckIfWeShouldRedirect(self, request: request_lib.HttpRequest):
        if not request.user.is_authenticated:
            return False
        if not request.user.CheckIfBanned():
            return False

    def process_view(self, request: request_lib.HttpRequest, callback, callback_args, callback_kwargs):
        if (
                getattr(callback, 'ban_ok', False)
                or not request.user.is_authenticated
                or not request.user.CheckIfBanned()):
            return None

        return redirect('users:banned')
