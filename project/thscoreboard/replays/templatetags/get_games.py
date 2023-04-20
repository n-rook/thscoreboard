"""Template tags used to get access to games."""

from typing import Iterable
from django import template
from replays import game_ids

from replays import models

register = template.Library()


PC98_GAME_IDS = {
    game_ids.GameIDs.TH01,
    game_ids.GameIDs.TH02,
    game_ids.GameIDs.TH03,
    game_ids.GameIDs.TH04,
    game_ids.GameIDs.TH05,
}


@register.simple_tag
def get_all_games_by_category() -> dict[str, list[models.Game]]:
    """Returns a list of all Touhou games by category (pc-98, windows, etc.), in a
    reasonable order."""
    all_games: Iterable[models.Game] = models.Game.objects.all()
    pc98_games = [game for game in all_games if game.game_id in PC98_GAME_IDS]
    windows_games = [game for game in all_games if game.game_id not in PC98_GAME_IDS]
    return {"PC-98": pc98_games, "Windows": windows_games}
