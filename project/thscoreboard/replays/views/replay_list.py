"""Contains views which list various replays."""

from typing import Optional

from django import urls
from django.views.decorators import http as http_decorators
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Manager
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
    return redirect(urls.reverse("Replays/GameScoreboard", args=[game_id]))


@http_decorators.require_safe
def game_scoreboard(
    request: WSGIRequest,
    game_id: str,
):
    game: Game = get_object_or_404(Game, game_id=game_id)
    filter_options = get_filter_options(game)
    show_route = game_id in [
        game_ids.GameIDs.TH01,
        game_ids.GameIDs.TH08,
        game_ids.GameIDs.TH128,
    ]

    return render(
        request,
        "replays/game_scoreboard.html",
        {
            "game": game,
            "filters": filter_options,
            "show_route": show_route,
        },
    )


def get_filter_options(game: Game) -> dict[str, list[str]]:
    if game.game_id == game_ids.GameIDs.TH01 or game.game_id == game_ids.GameIDs.TH128:
        return _get_filter_options_th01_th128(game)
    elif game.game_id == game_ids.GameIDs.TH08:
        return _get_filter_options_th08(game)
    elif game.game_id == game_ids.GameIDs.TH13:
        return _get_filter_options_th13(game)
    elif game.game_id == game_ids.GameIDs.TH16:
        return _get_filter_options_th16(game)
    elif game.game_id == game_ids.GameIDs.TH17:
        return _get_filter_options_th17(game)
    elif game.game_id == game_ids.GameIDs.TH20:
        return _get_filter_options_th20(game)
    else:
        return _get_filter_options_default(game)


def _get_filter_options_default(game: Game) -> dict[str, list[str]]:
    all_shots = [shot.GetName() for shot in Shot.objects.filter(game=game.game_id)]
    all_difficulties = [game.GetDifficultyName(d) for d in range(game.num_difficulties)]
    return {"Difficulty": all_difficulties, "Shot": all_shots}


def _get_filter_options_th01_th128(game: Game) -> dict[str, list[str]]:
    all_difficulties = [game.GetDifficultyName(d) for d in range(game.num_difficulties)]
    all_routes = [route.GetName() for route in Route.objects.filter(game=game.game_id)]
    return {"Difficulty": all_difficulties, "Route": all_routes}


def _get_filter_options_th08(game: Game) -> dict[str, list[str]]:
    all_shots = [shot.GetName() for shot in Shot.objects.filter(game=game.game_id)]
    all_difficulties = [game.GetDifficultyName(d) for d in range(game.num_difficulties)]
    all_routes = [route.GetName() for route in Route.objects.filter(game=game.game_id)]
    return {
        "Difficulty": all_difficulties,
        "Shot": all_shots,
        "Route": all_routes,
    }


def _get_filter_options_th13(game: Game) -> dict[str, list[str]]:
    filter_options = _get_filter_options_default(game)
    # The Overdrive difficulty only exists for spell practice, but we do not show any
    # spell practice replays.
    filter_options["Difficulty"].remove("Overdrive")
    return filter_options


def _get_filter_options_th16(game: Game) -> dict[str, list[str]]:
    all_characters = _deduplicate_list_preserving_order(
        shot.GetCharacterName() for shot in Shot.objects.filter(game=game.game_id)
    )
    all_seasons = _deduplicate_list_preserving_order(
        shot.GetSubshotName() for shot in Shot.objects.filter(game=game.game_id)
    )
    all_seasons.remove(None)
    all_difficulties = [game.GetDifficultyName(d) for d in range(game.num_difficulties)]
    return {
        "Difficulty": all_difficulties,
        "Character": all_characters,
        "Season": all_seasons,
    }


def _get_filter_options_th17(game: Game) -> dict[str, list[str]]:
    all_characters = _deduplicate_list_preserving_order(
        shot.GetCharacterName() for shot in Shot.objects.filter(game=game.game_id)
    )
    all_goasts = _deduplicate_list_preserving_order(
        shot.GetSubshotName() for shot in Shot.objects.filter(game=game.game_id)
    )
    all_difficulties = [game.GetDifficultyName(d) for d in range(game.num_difficulties)]
    return {
        "Difficulty": all_difficulties,
        "Character": all_characters,
        "Goast": all_goasts,
    }


def _get_filter_options_th20(game: Game) -> dict[str, list[str]]:
    all_characters = _deduplicate_list_preserving_order(
        shot.GetCharacterName() for shot in Shot.objects.filter(game=game.game_id)
    )
    all_stones = _deduplicate_list_preserving_order(
        shot.GetSubshotName() for shot in Shot.objects.filter(game=game.game_id)
    )
    all_difficulties = [game.GetDifficultyName(d) for d in range(game.num_difficulties)]
    return {
        "Difficulty": all_difficulties,
        "Character": all_characters,
        "Stone": all_stones,
    }


def _get_all_replay_for_game(game_id: str) -> Manager[models.Replay]:
    return (
        models.Replay.objects.prefetch_related("shot")
        .prefetch_related("route")
        .select_related("rank_view")
        .filter(category=models.Category.STANDARD)
        .filter(shot__game=game_id)
        .filter(replay_type=1)
        .filter(is_listed=True)
        .filter_visible()
        .order_by("-score")
    )


def _deduplicate_list_preserving_order(list_: list) -> list:
    deduplicated_list = []
    seen = set()
    for item in list_:
        if item not in seen:
            deduplicated_list.append(item)
            seen.add(item)
    return deduplicated_list
