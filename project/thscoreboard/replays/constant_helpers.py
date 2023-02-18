"""Utility functions to help deal with database-level constants like the Game table."""

import dataclasses
from typing import Optional

from replays import models


@dataclasses.dataclass(frozen=True)
class ReplayConstantModels:
    game: models.Game
    shot: models.Shot
    route: Optional[models.Route]


def GetModelInstancesForReplay(game: str, shot: str, route: str) -> ReplayConstantModels:
    """Get the constant model instances related to this replay."""
    shot = models.Shot.objects.select_related('game').get(game=game, shot_id=shot)
    if route:
        route = models.Route.objects.get(game=shot.game, route_id=route)
    else:
        route = None

    return ReplayConstantModels(
        game=shot.game,
        shot=shot,
        route=route
    )
