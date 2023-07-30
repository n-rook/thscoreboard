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


def get_pc98_games() -> list[models.Game]:
    all_games: Iterable[models.Game] = models.Game.objects.all()
    return [game for game in all_games if game.game_id in PC98_GAME_IDS]


def get_windows_games() -> list[models.Game]:
    all_games: Iterable[models.Game] = models.Game.objects.all()
    return [game for game in all_games if game.game_id not in PC98_GAME_IDS]


def get_all_games_by_category() -> dict[str, list[models.Game]]:
    """Returns a list of all Touhou games by category (pc-98, windows, etc.), in a
    reasonable order."""
    return {"PC-98": get_pc98_games(), "Windows": get_windows_games()}
