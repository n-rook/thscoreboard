import json
from typing import Iterable, Iterator
from functools import lru_cache

from replays import models, game_ids


class ReplayToJsonConverter:
    @lru_cache(maxsize=None)
    def _get_game(self, shot: models.Shot) -> models.Game:
        return shot.game

    @lru_cache(maxsize=None)
    def _get_shot_name(self, shot: models.Shot) -> str:
        return shot.GetName()

    def _convert_replay_to_dict(self, replay: models.Replay) -> dict:
        shot = replay.shot
        game = self._get_game(shot)
        score_prefix = _get_medal_emoji(replay.rank) if hasattr(replay, "rank") else ""

        json_dict = {}
        json_dict["Id"] = replay.id
        if replay.user:
            json_dict["User"] = {
                "text": f"{replay.user.username}",
                "url": f"/replays/user/{replay.user.username}",
            }
        else:
            json_dict["User"] = replay.imported_username or replay.name
        json_dict["Game"] = {
            "text": game.GetShortName(),
            "url": f"/replays/{game.game_id}",
        }
        json_dict["Difficulty"] = game_ids.GetDifficultyName(
            game.game_id, replay.difficulty
        )
        json_dict["Shot"] = self._get_shot_name(shot)
        if game.game_id in [game_ids.GameIDs.TH01, game_ids.GameIDs.TH08]:
            route = replay.route
            json_dict["Route"] = route.GetName() if route is not None else ""
        json_dict["Score"] = {
            "text": f"{score_prefix}{int(replay.score):,}",
            "url": f"/replays/{game.game_id}/{replay.id}",
        }
        json_dict["Upload Date"] = replay.created.strftime("%Y-%m-%d")
        json_dict["Comment"] = replay.GetShortenedComment()
        json_dict["Replay"] = {
            "text": "⬇",
            "url": f"/replays/{game.game_id}/{replay.id}/download",
        }

        if game.game_id == game_ids.GameIDs.TH16:
            json_dict |= self._get_th16_additional_fields(shot)
        elif game.game_id == game_ids.GameIDs.TH17:
            json_dict |= self._get_th17_additional_fields(shot)

        return json_dict

    def _get_th16_additional_fields(self, shot: models.Shot) -> dict:
        return {
            "Character": shot.GetCharacterName(),
            "Season": shot.GetSubshotName(),
        }

    def _get_th17_additional_fields(self, shot: models.Shot) -> dict:
        return {
            "Character": shot.GetCharacterName(),
            "Goast": shot.GetSubshotName(),
        }

    def convert_replays_to_serializable_list(
        self,
        ranked_replays: Iterable[models.Replay],
    ) -> Iterator[dict[str, any]]:
        for replay in ranked_replays:
            json_string = json.dumps(self._convert_replay_to_dict(replay))
            yield f"{json_string}\n".encode("utf-8")


def _get_medal_emoji(rank: int) -> str:
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    return ""
