"""The public page for a user's information."""


from django.contrib import auth
from django.shortcuts import get_object_or_404, render
from django.views.decorators import http as http_decorators

from replays import models


@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def user_page(request, username: str):
    user = get_object_or_404(auth.get_user_model(), username=username)
    
    def GetUserReplays():
        # Yields (game, list_of_replays_for_the_game) tuples.
        
        replays = (
            models.Replay.objects
            .filter(user=user)
            .exclude(category=models.Category.PRIVATE)
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
        request,
        'replays/user_page.html',
        {
            'viewed_user': user,
            'replays_by_game': list(GetUserReplays())
        }
    )
