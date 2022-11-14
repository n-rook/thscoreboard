"""A library used to create replays in the database.

This module works with the database and with parsed replay files, but
not with web entities like views or forms.
"""

from typing import Optional
from django.db import transaction

from replays import models
from replays import replay_parsing


@transaction.atomic
def PublishNewReplay(
        user,
        difficulty: int,
        shot: models.Shot,
        score: int,
        category: str,
        comment: str,
        video_link: str,
        is_good: bool,
        is_clear: bool,
        temp_replay_instance: models.TemporaryReplayFile,
        replay_info: replay_parsing.ReplayInfo):
    """Publish a new replay file.

    This creates a new Replay row, as well as rows in related tables like
    ReplayFile.

    Args:
        user: The User object who will own the new replay.
        difficulty: The difficulty of the new replay.
        shot: The Shot model instance for the replay.
        score: What score the run had at its end.
        category: The category for the replay (whether it's TAS, unlisted, etc.)
        comment: A string comment describing the replay from its creator.
        video_link: An optional link to a video of the replay.
        is_good: Whether the replay is valid (that is, whether it does not
            desync). If false, a video link is required.
        is_clear: Whether the replay cleared.
        temp_replay_instance: A TemporaryReplayFile model instance for the
            replay file. If the replay is published successfully, this is
            deleted.
        replay_info: The parsed replay info for the TemporaryReplayFile.

    Returns:
        The new Replay model instance.
    """
    replay_instance = models.Replay(
        user=user,
        shot=shot,
        difficulty=difficulty,
        score=score,
        category=category,
        comment=comment,
        video_link=video_link,
        is_good=is_good,
        is_clear=is_clear,
        rep_score=replay_info.score,
        timestamp=replay_info.timestamp,
        name=replay_info.name
    )
    replay_file_instance = models.ReplayFile(
        replay=replay_instance,
        replay_file=temp_replay_instance.replay,
    )

    replay_instance.save()
    replay_file_instance.save()
    temp_replay_instance.delete()

    for s in replay_info.stages:
        replay_stage = models.ReplayStage(
            replay=replay_instance,
            stage=s.stage,
            score=s.score,
            piv=s.piv,
            graze=s.graze,
            point_items=s.point_items,
            power=s.power,
            lives=s.lives,
            life_pieces=s.life_pieces,
            bombs=s.bombs,
            bomb_pieces=s.bomb_pieces,
            th06_rank=s.th06_rank,
            th07_cherry=s.th07_cherry,
            th07_cherrymax=s.th07_cherrymax
        )
        replay_stage.save()

    return replay_instance


def PublishReplayWithoutFile(
        user,
        difficulty: int,
        shot: models.Shot,
        score: int,
        category: str,
        comment: str,
        video_link: str,
        is_clear: bool,
        route: Optional[models.Route]):
    """Create a new Replay for a game in which replay files don't exist.

    Args:
        user: The User object who will own the new replay.
        difficulty: The difficulty of the new replay.
        shot: The Shot model instance for the replay.
        score: What score the run had at its end.
        category: The category for the replay (whether it's TAS, unlisted, etc.)
        comment: A string comment describing the replay from its creator.
        video_link: A link to a video of the replay.
        is_clear: Whether the replay cleared or not.
        route: Optional; if present, the game route taken in the run.

    Returns:
        The new Replay model instance.
    """
    replay_instance = models.Replay(
        user=user,
        shot=shot,
        difficulty=difficulty,
        route=route,
        score=score,
        category=category,
        is_clear=is_clear,
        comment=comment,
        video_link=video_link,
    )
    replay_instance.save()

    return replay_instance
