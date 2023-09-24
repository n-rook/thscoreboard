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


def GetReplayFileWithSameHash(
    file, include_ghosts=False
) -> Optional[models.ReplayFile]:
    """Return a replay file with the same hash is this one, if present.

    Args:
        file: The file data (bytes or memoryview).
        include_ghosts: If true, return "ghosts": replay files associated with
            deleted accounts (that is, accounts with is_active set to False).
            Ghosts are ignored for most purposes.

    Returns:
        The matching replay file, or None.
    """
    hash = CalculateReplayFileHash(file)
    q = models.ReplayFile.objects.filter(replay_hash=hash)
    if not include_ghosts:
        q = q.filter(replay__user__is_active=True)
    return q.first()


def CalculateReplayFileHash(file):
    return hashlib.sha256(file).digest()
