"""Reanalyze all replays."""

from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.shortcuts import render
from django.db import transaction
from django import urls

from replays import models
from replays import reanalyze_replay


# The number of replays to view and reanalyze at once.
# This must be low enough that the request will never take over 30 seconds,
# to avoid timeouts.
_BATCH_SIZE = 5000


def _ShortNameForReplay(r):
    return "{id} ({user}, {game})".format(
        id=r.id,
        user=r.user.username,
        game=r.shot.game.GetShortName(),
    )


def _select_next_replays_with_files(pagination_token, end_token=None):
    q = models.Replay.objects.filter(id__gt=pagination_token)
    if end_token is not None:
        q.filter(id__lte=end_token)
    return (
        q.select_related("shot", "shot__game")
        .filter(shot__game__has_replays=True)
        .order_by("id")[:_BATCH_SIZE]
    )


@http_decorators.require_http_methods(["GET", "HEAD"])
@auth_decorators.permission_required("staff", raise_exception=True)
def batch_reanalyze_preview(request, pagination_token: int = 0):
    """Preview the reanalysis of a page of replays."""

    replay_links = []

    # Bind r now so we can use it outside of the for loop.
    # This way, we can access the last element in the query without having to
    # conduct additional queries.
    r = None

    # To lessen the big load on the database, this view function is not
    # performed in one transaction.
    for r in _select_next_replays_with_files(pagination_token):
        # Typically in Django we would simply pass the replay instance to the
        # template engine, and define its rendering in the template. However,
        # since this method could easily return a very large number of replays,
        # we instead only keep the minimum information to render the replays
        # around.
        if reanalyze_replay.DoesReplayNeedUpdate(r.id):
            replay_links.append(
                {
                    "name": _ShortNameForReplay(r),
                    "url": urls.reverse(
                        viewname="Replays/Reanalysis", args=(r.shot.game_id, r.id)
                    ),
                }
            )

    if r:
        next_token = r.id
    else:
        # Since there are no replays, the "next token" is the same as the
        # current token.
        next_token = pagination_token

    more_pages = models.Replay.objects.filter(id__gt=next_token).exists()

    context = {
        "replays": replay_links,
        "current_token": pagination_token,
        "next_token": next_token,
        "more_pages": more_pages,
    }

    return render(
        request,
        "replays/reanalyze_batch.html",
        context,
    )


@http_decorators.require_http_methods(["POST"])
@auth_decorators.permission_required("staff", raise_exception=True)
def reanalyze_page(request, start_token: int, end_token: int):
    """Reanalyze replays, updating their metadata from the replay file.

    Args:
        start_token: A pagination token; an inclusive lower bound for the set
            of replays to be reanalyzed.
        end_token: A pagination token; an exclusive upper bound for the set of
            replays to be reanalyzed.
    """
    replay_links = []

    # To lessen the big load on the database, the updates are performed in many
    # small transactions, not one big one.
    for r in _select_next_replays_with_files(
        pagination_token=start_token, end_token=end_token
    ):
        if reanalyze_replay.DoesReplayNeedUpdate(r.id):
            with transaction.atomic():
                # The replay might have been deleted during this method's
                # resolution.
                if models.Replay.objects.filter(id=r.id).exists():
                    reanalyze_replay.UpdateReplay(r.id)
                    replay_links.append(
                        {
                            "name": _ShortNameForReplay(r),
                            "url": urls.reverse(
                                viewname="Replays/Details", args=(r.shot.game_id, r.id)
                            ),
                        }
                    )

    return render(
        request,
        "replays/successfully_reanalyzed_batch.html",
        {"replays": replay_links, "end_token": end_token},
    )
