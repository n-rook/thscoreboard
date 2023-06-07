from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Union
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from replays import forms
from replays.get_all_games import get_pc98_games, get_windows_games
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


def rankings(request: WSGIRequest) -> HttpResponse:
    selection = forms.RankingGameSelectionForm.DEFAULT_SELECTION
    form = forms.RankingGameSelectionForm(request.GET)
    if form.is_valid():
        selection = form.get_selection()
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
    game_ids = [game.game_id for game in games]
    top_3_replays = (
        replay_models.Replay.objects.filter(category=replay_models.Category.STANDARD)
        .filter(shot__game__in=game_ids)
        .filter(replay_type=1)
        .filter(is_listed=True)
        .annotate_with_rank()
        .filter(rank__lte=3)
    )

    for replay in top_3_replays:
        player = replay.user if replay.user is not None else replay.imported_username
        if replay.rank == 1:
            rankings[player].first_place_count += 1
        elif replay.rank == 2:
            rankings[player].second_place_count += 1
        else:
            rankings[player].third_place_count += 1
    return rankings


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
