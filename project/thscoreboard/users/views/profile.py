"""The user's own profile.

Currently, this page is fairly bare-boned. In the future, we will allow users
to do things like change their password or username here.
"""

from django.contrib.auth import decorators as auth_decorators
from django.shortcuts import render
from django.views.decorators import http as http_decorators

from users import forms


@auth_decorators.login_required
@http_decorators.require_safe
def profile(request):
    """View the user's profile page."""

    # The user profile is currently read-only, so we do not do anything for
    # POST requests yet.
    form = forms.UserProfileForm(
        initial={
            "username": request.user.username,
            "email": request.user.email,
            "password": "xxxxxxxxxx",
        }
    )

    return render(
        request,
        "users/profile.html",
        {
            "form": form,
        },
    )
