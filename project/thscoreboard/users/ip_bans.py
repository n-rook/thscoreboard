"""Contains general modules related to IP bans."""

from ipaddress import ip_address, ip_network
from functools import wraps

from django.http import HttpResponseForbidden

from users import models


def check_ip_bans(methods_to_check: list):
    """Returns a decorator that prevents access by IP-banned clients.

    Args:
        methods_to_check: A list of HTTP methods (like "GET" or "POST") for which to enforce
            the ban.

    Returns:
        A decorator which returns 403 for IP-banned users.
    """

    def is_ip_banned(ip_to_check: str):
        request_ip = ip_address(ip_to_check)
        return any(request_ip in ip_network(ip.ip) for ip in models.IPBan.objects.all())

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method in methods_to_check and is_ip_banned(
                request.META.get("REMOTE_ADDR")
            ):
                return HttpResponseForbidden(content="Your IP address is banned")
            return func(request, *args, **kwargs)

        return inner

    return decorator
