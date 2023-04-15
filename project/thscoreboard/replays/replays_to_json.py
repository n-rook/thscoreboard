from typing import Iterable
from replays import models, game_ids
from functools import lru_cache


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
        json_dict = {
            "Id": replay.id,
            "User": {
                "text": f"{replay.user.username}",
                "url": f"/replays/user/{replay.user.username}",
            }
            if replay.user
            else replay.imported_username or replay.name,
            "Game": game.GetShortName(),
            "Difficulty": game_ids.GetDifficultyName(game.game_id, replay.difficulty),
            "Shot": self._get_shot_name(shot),
            "Score": {
                "text": f"{int(replay.score):,}",
                "url": f"/replays/{game.game_id}/{replay.id}",
            },
            "Upload Date": replay.created.strftime("%Y-%m-%d"),
            "Comment": replay.GetShortenedComment(),
            "Replay": {
                "text": "⬇",
                "url": f"/replays/{game.game_id}/{replay.id}/download",
            },
        }

        if game.game_id == game_ids.GameIDs.TH08:
            json_dict |= self._get_th08_additional_fields(replay)

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
    
    def _get_th08_additional_fields(self, replay: models.Replay) -> dict:
        route = replay.route
        if route is None:
            return {}
        return {"Route": replay.route.GetName()}

    def convert_replays_to_serializable_list(
        self,
        replays: Iterable[models.Replay],
    ) -> list[dict[str, any]]:
        return [self._convert_replay_to_dict(replay) for replay in replays]
