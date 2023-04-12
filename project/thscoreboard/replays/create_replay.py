"""A library used to create replays in the database.

This module works with the database and with parsed replay files, but
not with web entities like views or forms.
"""

import datetime
from typing import Optional
from django.db import transaction

from replays import constant_helpers
from replays import game_ids
from replays import models
from replays import replay_parsing


@transaction.atomic
def PublishNewReplay(
    user,
    difficulty: int,
    score: int,
    category: str,
    comment: str,
    video_link: str,
    is_good: bool,
    is_clear: bool,
    no_bomb: Optional[bool],
    miss_count: Optional[int],
    temp_replay_instance: models.TemporaryReplayFile,
    replay_info: replay_parsing.ReplayInfo,
    created_timestamp: Optional[datetime.datetime] = None,
    imported_username: Optional[str] = None,
):
    """Publish a new replay file.

    This creates a new Replay row, as well as rows in related tables like
    ReplayFile.

    Args:
        user: The User object who will own the new replay.
        difficulty: The difficulty of the new replay.
        score: What score the run had at its end.
        category: The category for the replay (whether it's TAS, unlisted, etc.)
        comment: A string comment describing the replay from its creator.
        video_link: An optional link to a video of the replay.
        is_good: Whether the replay is valid (that is, whether it does not
            desync). If false, a video link is required.
        is_clear: Whether the replay cleared.
        no_bomb: Whether the replay is NB. Can be None, but only if it is not
            applicable to the game or replay type.
        miss_count: The number of misses in the replay. May be None if the user
            chose not to specify this.
        temp_replay_instance: A TemporaryReplayFile model instance for the
            replay file. If the replay is published successfully, this is
            deleted.
        replay_info: The parsed replay info for the TemporaryReplayFile.
        created_timestamp: When the replay was uploaded. Defaults to now.
        imported_username: The user who uploaded the replay to an extrenal
            site, such as royalflare.

    Returns:
        The new Replay model instance.
    """
    constants = constant_helpers.GetModelInstancesForReplay(replay_info)
    replay_instance = models.Replay(
        user=user,
        difficulty=difficulty,
        score=score,
        category=category,
        comment=comment,
        video_link=video_link,
        is_good=is_good,
        is_clear=is_clear,
        created=created_timestamp or datetime.datetime.now(tz=datetime.timezone.utc),
        imported_username=imported_username,
    )
    replay_instance.SetFromReplayInfo(replay_info)
    replay_instance.SetForeignKeysFromConstantModels(constants)
    if game_ids.HasBombs(replay_info.game, replay_info.replay_type):
        if no_bomb is None:
            raise ValueError("no_bomb is required if applicable")
        replay_instance.no_bomb = no_bomb
    if game_ids.HasLives(replay_info.game, replay_info.replay_type):
        replay_instance.miss_count = miss_count

    replay_file_instance = models.ReplayFile(
        replay=replay_instance,
        replay_file=temp_replay_instance.replay,
        replay_hash=constant_helpers.CalculateReplayFileHash(
            temp_replay_instance.replay
        ),
    )

    replay_instance.save()
    replay_file_instance.save()
    temp_replay_instance.delete()

    for s in replay_info.stages:
        #   th09 shot foreign key
        th09_shot_instance = None
        if replay_info.game == game_ids.GameIDs.TH09:
            th09_shot_instance = models.Shot.objects.select_related("game").get(
                game=game_ids.GameIDs.TH09, shot_id=s.th09_p2_shot
            )

        replay_stage = models.ReplayStage(
            replay=replay_instance, stage=s.stage, th09_p2_shot=th09_shot_instance
        )
        replay_stage.SetFromReplayStageInfo(s)
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
    replay_type: int,
    route: Optional[models.Route],
    no_bomb: Optional[bool],
    miss_count: Optional[int],
):
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
        no_bomb: Whether the replay is NB. Can be None, but only if it is not
            applicable to the game or replay type.
        miss_count: The number of misses in the replay. May be None if the user
            chose not to specify this.

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
        replay_type=replay_type,
        created=datetime.datetime.now(tz=datetime.timezone.utc),
    )
    if game_ids.HasBombs(shot.game_id, replay_type):
        if no_bomb is None:
            raise ValueError("no_bomb is required if applicable")
        replay_instance.no_bomb = no_bomb
    if game_ids.HasLives(shot.game_id, replay_type):
        replay_instance.miss_count = miss_count
    replay_instance.save()

    return replay_instance
