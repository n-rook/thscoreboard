"""Contains views which list various replays."""

import json
from typing import Optional

from django import urls
from django.views.decorators import http as http_decorators
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Manager, Q
from django.core.handlers.wsgi import WSGIRequest

from replays import models
from replays import game_ids
from replays.models import Game, Shot, Route
from replays.replays_to_json import convert_replays_to_json_bytes
from replays.views.replay_table_helpers import stream_json_bytes_to_http_reponse


@http_decorators.require_safe
def game_scoreboard_json(request: WSGIRequest, game_id: str):
    replays = _get_all_replay_for_game(game_id)
    replay_jsons = convert_replays_to_json_bytes(replays)
    return stream_json_bytes_to_http_reponse(replay_jsons)


def game_scoreboard_old_url(
    request: WSGIRequest, game_id: str, difficulty: int, shot_id: Optional[str] = None
):
    """Redirect requests going to the old filtered game scoreboard URLs.

    We still get occasional requests to these URLs.

    Note that the extra parameters are currently ignored. If we add query
    strings or similar filter representations to the game scoreboard page, we
    should update this function to use them.

    Args:
        request: The request object.
        game_id: The game ID the user is interested in viewing.
        difficulty: An integer corresponding to the replay difficulty to display.
        shot_id: The shot ID the user is interested in viewing.
    """
    return redirect(
        urls.reverse("Replays/GameScoreboard", args=[game_id])
    )


@http_decorators.require_safe
def game_scoreboard(
    request: WSGIRequest,
    game_id: str,
):
    difficulty = request.GET.get("difficulty", None)
    shot_id = request.GET.get("shot", None)
    route = request.GET.get("route", None)

    game: Game = get_object_or_404(Game, game_id=game_id)
    filter_options = get_filter_options(game)
    show_route = game_id in [
        game_ids.GameIDs.TH01,
        game_ids.GameIDs.TH08,
        game_ids.GameIDs.TH128,
    ]
    starting_filters = get_starting_filters(
        filter_options, game, difficulty, shot_id, route
    )

    return render(
        request,
        "replays/game_scoreboard.html",
        {
            "game": game,
            "filters": filter_options,
            "show_route": show_route,
            "starting_filters": starting_filters,
        },
    )


def get_filter_options(game: Game) -> dict[str, list[str]]:
    filter_options = {}
    filter_options["Difficulty"] = [
        game.GetDifficultyName(d) for d in range(game.num_difficulties)
    ]

    if game.has_routes:
        filter_options["Route"] = [
            route.GetName() for route in Route.objects.filter(game=game.game_id)
        ]

    if game.has_multiple_shots:
        if game.has_subshots:
            all_characters = _deduplicate_list_preserving_order(
                shot.GetCharacterName()
                for shot in Shot.objects.filter(game=game.game_id)
            )
            all_subshots = _deduplicate_list_preserving_order(
                shot.GetSubshotName() for shot in Shot.objects.filter(game=game.game_id)
            )
            if None in all_subshots:
                all_subshots.remove(None)
            filter_options["Character"] = all_characters
            filter_options["Subshot"] = all_subshots
        else:
            filter_options["Shot"] = [
                shot.GetName() for shot in Shot.objects.filter(game=game.game_id)
            ]

    if game.game_id == game_ids.GameIDs.TH13:
        # The Overdrive difficulty only exists for spell practice, but we do not show
        # any spell practice replays.
        filter_options["Difficulty"].remove("Overdrive")

    return filter_options


def get_starting_filters(
    filter_options: dict[str, list[str]],
    game: Game,
    difficulty: Optional[str],
    shot_id: Optional[str],
    route: Optional[str],
) -> dict[str, str]:
    starting_filters = {filter_type: "All" for filter_type in filter_options.keys()}
    if difficulty is not None:
        starting_filters["Difficulty"] = game.GetDifficultyName(int(difficulty))
    if route is not None:
        starting_filters["Route"] = route
    if shot_id is not None:
        shot = Shot.objects.get(game=game.game_id, shot_id__iexact=shot_id)
        if game.has_subshots:
            starting_filters["Character"] = shot.GetCharacterName()
            starting_filters["Subshot"] = shot.GetSubshotName()
        else:
            starting_filters["Shot"] = shot.GetName()
    return starting_filters


def _get_all_replay_for_game(game_id: str) -> Manager[models.Replay]:
    return (
        models.Replay.objects.prefetch_related("shot")
        .prefetch_related("route")
        .filter(category=models.Category.STANDARD)
        .filter(shot__game=game_id)
        .filter(replay_type=1)
        .filter(is_listed=True)
        .filter_visible()
        .order_by("-score")
        .annotate_with_rank()
    )


def _deduplicate_list_preserving_order(list_: list) -> list:
    deduplicated_list = []
    seen = set()
    for item in list_:
        if item not in seen:
            deduplicated_list.append(item)
            seen.add(item)
    return deduplicated_list
