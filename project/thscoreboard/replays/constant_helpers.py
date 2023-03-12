"""Utility functions to help deal with database-level constants like the Game table."""

import dataclasses
from typing import Optional

from replays import models
from replays import replay_parsing
import hashlib


@dataclasses.dataclass(frozen=True)
class ReplayConstantModels:
    game: models.Game
    shot: models.Shot
    route: Optional[models.Route]


def GetModelInstancesForReplay(replay_info: replay_parsing.ReplayInfo) -> ReplayConstantModels:
    """Get the constant model instances related to this replay."""
    shot = models.Shot.objects.select_related('game').get(game=replay_info.game, shot_id=replay_info.shot)
    if replay_info.route:
        route = models.Route.objects.get(game=shot.game, route_id=replay_info.route)
    else:
        route = None

    return ReplayConstantModels(
        game=shot.game,
        shot=shot,
        route=route
    )


def CheckReplayFileDuplicate(file):
    hash = CalculateReplayFileHash(file)
    return models.ReplayFile.objects.filter(replay_hash=hash).exists()


def CalculateReplayFileHash(file):
    return hashlib.sha256(file).digest()
