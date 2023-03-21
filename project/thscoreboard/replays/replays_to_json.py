import json
from typing import Iterable
from replays import models


def convert_replays_to_json_string(replays: Iterable[models.Replay]) -> str:
    replay_dicts = [
        {
            "User": replay.user.username,
            "Game": replay.shot.game.GetShortName(),
            "Difficulty": replay.GetDifficultyName(),
            "Shot": replay.shot.GetName(),
            "Score": {
                "text": f"{int(replay.score):,}",
                "url": f"/replays/{replay.shot.game.game_id}/{replay.id}",
            },
            "Upload Date": replay.created.strftime("%Y-%m-%d"),
            "Replay": {
                "text": "Download",
                "url": f"/replays/{replay.shot.game.game_id}/{replay.id}",
            },
        }
        for replay in replays
    ]
    return json.dumps(replay_dicts)
