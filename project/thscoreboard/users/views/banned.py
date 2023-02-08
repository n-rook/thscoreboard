"""The user's own profile.

Currently, this page is fairly bare-boned. In the future, we will allow users
to do things like change their password or username here.
"""

from django.contrib.auth import decorators as auth_decorators
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators import http as http_decorators

from users import models
from users.middleware import check_ban


@auth_decorators.login_required
@http_decorators.require_safe
@check_ban.allow_access_by_banned_users
def banned_notification(request):
    """Inform the user why they are banned."""

    with transaction.atomic():
        if not request.user.CheckIfBanned():
            # The user is not banned, just send them to the homepage.
            return redirect('/')

        latest_ban = models.Ban.objects.filter(target=request.user).order_by('-expiration')[0]

    return render(
        request,
        'users/banned.html',
        {
            'reason': latest_ban.reason,
            'expiration': latest_ban.expiration,
        }
    )
