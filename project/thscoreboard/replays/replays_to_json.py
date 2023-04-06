from typing import Iterable
from replays import models


def convert_replays_to_serializable_list(
    replays: Iterable[models.Replay],
) -> list[dict[str, any]]:
    replay_dicts = [
        {
            "Id": replay.id,
            "User": {
                "text": f"{replay.user.username}",
                "url": f"/replays/user/{replay.user.username}",
            }
            if replay.user
            else replay.imported_username or replay.name,
            "Game": replay.shot.game.GetShortName(),
            "Difficulty": replay.GetDifficultyName(),
            "Shot": replay.shot.GetName(),
            "Score": {
                "text": f"{int(replay.score):,}",
                "url": f"/replays/{replay.shot.game.game_id}/{replay.id}",
            },
            "Upload Date": replay.created.strftime("%Y-%m-%d"),
            "Comment": replay.GetShortenedComment(),
            "Replay": {
                "text": "Download",
                "url": f"/replays/{replay.shot.game.game_id}/{replay.id}",
            },
        }
        for replay in replays
    ]
    return replay_dicts
