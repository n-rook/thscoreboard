"""The user's own profile.

Currently, this page is fairly bare-boned. In the future, we will allow users
to do things like change their password or username here.
"""

from django.contrib.auth import decorators as auth_decorators
from django.shortcuts import render
from django.views.decorators import http as http_decorators

from users import forms
from replays import models


@auth_decorators.login_required
@http_decorators.require_safe
def profile(request):
    """View the user's profile page."""
    
    # The user profile is currently read-only, so we do not do anything for
    # POST requests yet.
    form = forms.UserProfileForm(
        initial={
            'username': request.user.username,
            'email': request.user.email,
            'password': 'xxxxxxxxxx'
        }
    )

    def GetPendingReplays():
        # Yields (game, list_of_replays_for_the_game) tuples.

        replays = (
            models.Replay.objects
            .filter(user=request.user, category=models.Category.PENDING)
            .order_by('shot__game_id', 'shot_id', 'created'))

        current_game = None
        for replay in replays:
            if current_game is None:
                current_game = replay.shot.game
                current_replays = []
            if current_game != replay.shot.game:
                yield (current_game, current_replays)
                current_game = replay.shot.game
                current_replays = []
            current_replays.append(replay)
        if current_game is not None:
            yield (current_game, current_replays)

    return render(
        request, 'users/profile.html',
        {
            'form': form,
            'pending_replays': list(GetPendingReplays())
        })
