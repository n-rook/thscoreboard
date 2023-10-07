from typing import Iterable

from replays import game_ids
from replays import models


PC98_GAME_IDS = [
    game_ids.GameIDs.TH01,
    game_ids.GameIDs.TH02,
    game_ids.GameIDs.TH03,
    game_ids.GameIDs.TH04,
    game_ids.GameIDs.TH05,
]

CLASSIC_GAME_IDS = [
    game_ids.GameIDs.TH06,
    game_ids.GameIDs.TH07,
    game_ids.GameIDs.TH08,
    game_ids.GameIDs.TH09,
]

DIVINE_CYCLE_GAME_IDS = [
    game_ids.GameIDs.TH10,
    game_ids.GameIDs.TH11,
    game_ids.GameIDs.TH12,
    game_ids.GameIDs.TH13,
    game_ids.GameIDs.TH128,
]

NEW_GAME_IDS = [
    game_ids.GameIDs.TH14,
    game_ids.GameIDs.TH15,
    game_ids.GameIDs.TH16,
    game_ids.GameIDs.TH17,
    game_ids.GameIDs.TH18,
]


def get_pc98_games() -> list[models.Game]:
    all_games: Iterable[models.Game] = models.Game.objects.all()
    return [game for game in all_games if game.game_id in PC98_GAME_IDS]


def get_windows_games() -> list[models.Game]:
    all_games: Iterable[models.Game] = models.Game.objects.all()
    return [game for game in all_games if game.game_id not in PC98_GAME_IDS]


def get_all_games_by_category() -> dict[str, list[models.Game]]:
    """Returns all Touhou games, organized by category.

    The categories are fairly arbitrary, and are not intended to be used for
    more than visually categorizing and separating games.

    Returns:
        A dict from "category IDs" (strings) to lists of Games. The dictionary
        is ordered in a reasonable order for the games to be listed.
    """
    all_games_by_id = {g.game_id: g for g in models.Game.objects.all()}

    def GamesIn(id_list):
        return [all_games_by_id[game_id] for game_id in id_list]

    return {
        "PC-98": GamesIn(PC98_GAME_IDS),
        "Classic": GamesIn(CLASSIC_GAME_IDS),
        "Divine": GamesIn(DIVINE_CYCLE_GAME_IDS),
        "New": GamesIn(NEW_GAME_IDS),
    }
