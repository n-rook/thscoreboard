from collections import defaultdict
from typing import Iterable
from replays import models, game_ids
from functools import lru_cache


class ReplayToJsonConverter:
    def __init__(self, include_medals=False) -> None:
        self.include_medals = include_medals
        self.replay_count_by_category: dict[tuple[int, models.Shot], int] = defaultdict(
            int
        )

    @lru_cache(maxsize=None)
    def _get_game(self, shot: models.Shot) -> models.Game:
        return shot.game

    @lru_cache(maxsize=None)
    def _get_shot_name(self, shot: models.Shot) -> str:
        return shot.GetName()

    def _convert_replay_to_dict(self, replay: models.Replay) -> dict:
        shot = replay.shot
        game = self._get_game(shot)
        difficulty = replay.difficulty

        score_prefix = ""
        if self.include_medals:
            self._update_replay_count_by_category(difficulty, shot)
            rank = self.replay_count_by_category[(difficulty, shot)]
            score_prefix = _get_medal_emoji(rank)

        json_dict = {}
        json_dict["Id"] = replay.id
        if replay.user:
            json_dict["User"] = {
                "text": f"{replay.user.username}",
                "url": f"/replays/user/{replay.user.username}",
            }
        else:
            json_dict["User"] = replay.imported_username or replay.name
        json_dict["Game"] = game.GetShortName()
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

    def _update_replay_count_by_category(self, difficulty: int, shot: models.Shot):
        self.replay_count_by_category[(difficulty, shot)] += 1

    def convert_replays_to_serializable_list(
        self,
        replays: Iterable[models.Replay],
    ) -> list[dict[str, any]]:
        return [self._convert_replay_to_dict(replay) for replay in replays]


def _get_medal_emoji(rank: int) -> str:
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    return ""
