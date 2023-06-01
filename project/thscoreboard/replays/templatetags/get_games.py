"""Template tags used to get access to games."""

from django import template

from replays import get_all_games
from replays import models

register = template.Library()


@register.simple_tag
def get_all_games_by_category() -> dict[str, list[models.Game]]:
    return get_all_games.get_all_games_by_category()
