"""Reanalyze all replays."""

from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.shortcuts import render
from django.db import transaction
from django import urls

from replays import models
from replays import reanalyze_replay


def _ShortNameForReplay(r):
    return '{id} ({user}, {game})'.format(
        id=r.id,
        user=r.user.username,
        game=r.shot.game.GetShortName(),
    )


def _select_all_replays_with_files():
    return (
        models.Replay.objects
        .select_related('shot', 'shot__game')
        .filter(shot__game__has_replays=True))


@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
@auth_decorators.permission_required('staff', raise_exception=True)
def reanalyze_all(request):
    if request.method == 'POST':
        return _post_reanalyze_all(request)
    else:
        return _get_reanalyze_all(request)


def _get_reanalyze_all(request):
    # This request is likely to be extremely expensive. At some point,
    # we'll want to adjust it to be cheaper.

    replay_links = []

    # To lessen the big load on the database, this view function is not
    # performed in one transaction.
    for r in _select_all_replays_with_files():
        # Typically in Django we would simply pass the replay instance to the
        # template engine, and define its rendering in the template. However,
        # since this method could easily return a very large number of replays,
        # we instead only keep the minimum information to render the replays
        # around.
        if reanalyze_replay.DoesReplayNeedUpdate(r.id):
            replay_links.append({
                'name': _ShortNameForReplay(r),
                'url': urls.reverse(
                    viewname='Replays/Reanalysis',
                    args=(r.shot.game_id, r.id))
            })

    return render(
        request,
        'replays/reanalyze_all.html',
        {
            'replays': replay_links,
        }
    )


def _post_reanalyze_all(request):
    replay_links = []

    # To lessen the big load on the database, the updates are performed in many
    # small transactions, not one big one.
    for r in _select_all_replays_with_files():
        if reanalyze_replay.DoesReplayNeedUpdate(r.id):
            with transaction.atomic():
                # The replay might have been deleted during this method's
                # resolution.
                if models.Replay.objects.filter(id=r.id).exists():
                    reanalyze_replay.UpdateReplay(r.id)
                    replay_links.append({
                        'name': _ShortNameForReplay(r),
                        'url': urls.reverse(
                            viewname='Replays/Details',
                            args=(r.shot.game_id, r.id)
                        ),
                    })

    return render(
        request,
        'replays/successfully_reanalyzed_all.html',
        {
            'replays': replay_links
        }
    )
