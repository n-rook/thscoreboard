from collections import defaultdict
from dataclasses import dataclass
import itertools
from typing import Iterable, Union
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators import http as http_decorators

from replays import forms
from replays.get_all_games import get_pc98_games, get_windows_games
from replays.views.replay_list import get_all_replay_for_game
import users.models as user_models
import replays.models as replay_models


@dataclass
class RankCount:
    first_place_count: int
    second_place_count: int
    third_place_count: int

    def __lt__(self, other):
        return (
            self.first_place_count,
            self.second_place_count,
            self.third_place_count,
        ) < (other.first_place_count, other.second_place_count, other.third_place_count)


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def rankings(request: WSGIRequest) -> HttpResponse:
    selection = forms.RankingGameSelectionForm.DEFAULT_SELECTION
    if request.method == "POST":
        form = forms.RankingGameSelectionForm(request.POST)
        if form.is_valid():
            selection = (
                form.cleaned_data["grouped_game_selection"]
                or form.cleaned_data["pc98_game_selection"]
                or form.cleaned_data["windows_game_selection"]
            )
    games = _get_all_games_from_selection(selection)

    rankings = _get_all_player_rankings_for_games(games)
    rankings_dicts = _rankings_to_dicts(rankings)
    game_selection_form = forms.RankingGameSelectionForm()
    return render(
        request,
        "users/rankings.html",
        {
            "rankings": rankings_dicts,
            "form": game_selection_form,
            "selection": selection,
        },
    )


def _get_all_player_rankings_for_games(
    games: Iterable[replay_models.Game],
) -> dict[str | user_models.User, RankCount]:
    rankings = defaultdict(lambda: RankCount(0, 0, 0))
    for game in games:
        all_replays = get_all_replay_for_game(game)
        all_ranked_categories = _get_all_ranked_categories_for_game(game)
        for shot, difficulty, route in all_ranked_categories:
            top_3_replays = all_replays.filter(
                shot=shot, difficulty=difficulty, route=route
            )[:3]
            rankings = _update_rankings(rankings, top_3_replays)
    return rankings


def _update_rankings(
    rankings: dict[Union[str, user_models.User], RankCount],
    top_3_replays: Iterable[replay_models.Replay],
) -> dict[Union[str, user_models.User], RankCount]:
    for replay_rank, replay in enumerate(top_3_replays):
        player_name = (
            replay.user if replay.user is not None else replay.imported_username
        )
        if replay_rank == 0:
            rankings[player_name].first_place_count += 1
        elif replay_rank == 1:
            rankings[player_name].second_place_count += 1
        else:
            rankings[player_name].third_place_count += 1
    return rankings


def _get_all_ranked_categories_for_game(
    game: replay_models.Game,
) -> Iterable[tuple[replay_models.Shot, int, replay_models.Route]]:
    # Excludes unranked categories, such as replays that have no route due to early game-overs.

    all_shots = replay_models.Shot.objects.filter(game=game)
    all_difficulties = list(range(game.num_difficulties))
    all_routes = replay_models.Route.objects.filter(game=game)
    if len(all_routes) == 0:
        all_routes = [None]
    if len(all_shots) == 0:
        all_shots = [None]
    return itertools.product(all_shots, all_difficulties, all_routes)


def _rankings_to_dicts(
    rankings: list[tuple[Union[str, user_models.User], RankCount]]
) -> list[dict]:
    rows = []
    sorted_ranking_items = sorted(
        rankings.items(), key=lambda item: item[1], reverse=True
    )
    for i, (user, rank_count) in enumerate(sorted_ranking_items):
        row = {
            "player_rank": i + 1,  # Make displayed numbers be 1-indexed
            "first_place_count": rank_count.first_place_count,
            "second_place_count": rank_count.second_place_count,
            "third_place_count": rank_count.third_place_count,
        }
        if isinstance(user, str):
            row["username"] = user
        else:
            row["user"] = user
        rows.append(row)
    return rows


def _get_all_games_from_selection(selection: str) -> Iterable[replay_models.Game]:
    games = replay_models.Game.objects.filter(game_id=selection)
    if len(games) == 1:
        return games

    if selection == forms.RankingGameSelectionForm.SELECT_ALL:
        return replay_models.Game.objects.all()
    if selection == forms.RankingGameSelectionForm.SELECT_PC98:
        return get_pc98_games()
    if selection == forms.RankingGameSelectionForm.SELECT_WINDOWS:
        return get_windows_games()
