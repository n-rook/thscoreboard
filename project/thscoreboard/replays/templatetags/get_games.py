"""Template tags used to get access to games."""

from django import template

from replays import models

register = template.Library()


@register.simple_tag
def get_all_games():
    """Returns a list of all Touhou games, in a reasonable order."""
    return models.Game.objects.all()
