"""Makes some replays available for tests."""

import datetime
from pathlib import Path
import typing

from replays import create_replay
from replays import game_ids
from replays import models
from replays import replay_parsing


TEST_REPLAY_LOCATION = Path("replays/replays_for_tests")

_filename_type = typing.Literal[
    "th6_extra", "th6_hard_1cc", "th7_lunatic", "th10_normal"
]
"""A special literal type which defines all possible filenames.

Why bother with this? Well, it gets most IDEs to autocomplete these values,
which is very convenient!
"""


def GetRaw(filename: _filename_type) -> bytes:
    """Read and return a test replay as bytes.

    Args:
        filename: The first part of the filename (before ".rpy").

    Returns:
        The file, in bytes.
    """
    true_filename = f"{filename}.rpy"

    with open(TEST_REPLAY_LOCATION / true_filename, "rb") as f:
        return f.read()


def CreateAsPublishedReplay(
    filename: _filename_type,
    user=None,
    difficulty=None,
    score=None,
    category=models.Category.STANDARD,
    comment="",
    is_good=True,
    is_clear=True,
    video_link="",
    no_bomb=False,
    miss_count=None,
    created_timestamp: typing.Optional[datetime.datetime] = None,
    imported_username: typing.Optional[str] = None,
    replay_type: typing.Optional[models.ReplayType] = None,
):
    """Create a replay according to a file, with sensible defaults."""

    replay_file_contents = GetRaw(filename)
    temp_replay = models.TemporaryReplayFile(user=user, replay=replay_file_contents)
    temp_replay.save()

    replay_info = replay_parsing.Parse(replay_file_contents)
    if replay_type is not None:
        replay_info.replay_type = replay_type

    if difficulty is None:
        difficulty = replay_info.difficulty
    if score is None:
        score = replay_info.score

    return create_replay.PublishNewReplay(
        user=user,
        difficulty=difficulty,
        score=score,
        category=category,
        comment=comment,
        is_good=is_good,
        is_clear=is_clear,
        video_link=video_link,
        temp_replay_instance=temp_replay,
        replay_info=replay_info,
        no_bomb=no_bomb,
        miss_count=miss_count,
        created_timestamp=created_timestamp,
        imported_username=imported_username,
    )


def CreateReplayWithoutFile(
    user,
    shot,
    difficulty,
    score,
    route=None,
    category=models.Category.STANDARD,
    comment="",
    is_clear=True,
    video_link="",
    no_bomb=False,
    miss_count=None,
    replay_type: models.ReplayType = game_ids.ReplayTypes.FULL_GAME,
):
    """Create a replay without a file (for things like PC-98 replays)."""

    return create_replay.PublishReplayWithoutFile(
        user=user,
        difficulty=difficulty,
        shot=shot,
        score=score,
        route=route,
        category=category,
        comment=comment,
        is_clear=is_clear,
        video_link=video_link,
        replay_type=replay_type,
        no_bomb=no_bomb,
        miss_count=miss_count,
    )
