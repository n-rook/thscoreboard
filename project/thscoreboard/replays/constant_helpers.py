"""Utility functions to help deal with database-level constants like the Game table."""

from __future__ import annotations

import dataclasses
from typing import Optional

from django import apps

from replays import replay_parsing
import hashlib
from replays import models


def _Route():
    return apps.apps.get_model("replays", "Route")


def _Shot():
    return apps.apps.get_model("replays", "Shot")


@dataclasses.dataclass(frozen=True)
class ReplayConstantModels:
    game: models.Game
    shot: models.Shot
    route: Optional[models.Route]


def GetModelInstancesForReplay(
    replay_info: replay_parsing.ReplayInfo,
) -> models.ReplayConstantModels:
    """Get the constant model instances related to this replay."""
    shot = (
        _Shot()
        .objects.select_related("game")
        .get(game=replay_info.game, shot_id=replay_info.shot)
    )
    if replay_info.route:
        route = _Route().objects.get(game=shot.game, route_id=replay_info.route)
    else:
        route = None

    return ReplayConstantModels(game=shot.game, shot=shot, route=route)


def CheckReplayFileDuplicate(file):
    hash = CalculateReplayFileHash(file)
    return models.ReplayFile.objects.filter(replay_hash=hash).exists()


def CalculateReplayFileHash(file):
    return hashlib.sha256(file).digest()
