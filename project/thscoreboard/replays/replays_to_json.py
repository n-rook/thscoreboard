import json
from typing import Any, Iterable, Optional
from functools import lru_cache
import urllib.parse

from django.core.serializers import json as django_json
from django.utils.functional import Promise

from replays import models, game_ids


class ReplayToJsonConverter:
    @lru_cache(maxsize=None)
    def _get_game(self, shot: models.Shot) -> models.Game:
        return shot.game

    @lru_cache(maxsize=None)
    def _get_shot_name(self, shot: models.Shot) -> str:
        return shot.GetName()

    def convert_replay_to_dict(self, replay: models.Replay) -> dict:
        shot = replay.shot
        game = self._get_game(shot)

        rank = replay.GetRank()
        if rank is None:
            score_prefix = ""
        else:
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
        json_dict["Game"] = {
            "text": game.GetShortName(),
            "url": create_leaderboard_url(game.game_id),
        }
        json_dict["Difficulty"] = {
            "text": game_ids.GetDifficultyName(game.game_id, replay.difficulty),
            "url": create_leaderboard_url(game.game_id, replay.difficulty),
        }
        json_dict["Shot"] = {
            "text": self._get_shot_name(shot),
            "url": create_leaderboard_url(
                game.game_id, replay.difficulty, shot.shot_id
            ),
        }
        if game.has_routes:
            route = replay.route
            route_name = route.GetName() if route is not None else ""
            route_id = route.route_id if route is not None else ""
            json_dict["Route"] = {
                "text": route_name,
                "url": create_leaderboard_url(
                    game.game_id, replay.difficulty, shot.shot_id, route_id
                ),
            }
        if game.game_id == game_ids.GameIDs.TH128 and replay.difficulty == 4:
            json_dict["Route"] = "Extra"
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

        if game.has_subshots:
            json_dict["Character"] = shot.GetCharacterName()
            json_dict["Subshot"] = shot.GetSubshotName()

        return json_dict

    def convert_replay_to_json_bytes(self, replay: models.Replay) -> bytes:
        replay_dict = self.convert_replay_to_dict(replay)
        json_str = json.dumps(replay_dict, cls=_LazyDjangoJSONEncoder)
        return f"{json_str}\n".encode("utf-8")


def create_leaderboard_url(
    game_id: str,
    difficulty_id: Optional[int] = None,
    shot_id: Optional[str] = None,
    route_id: Optional[str] = None,
) -> str:
    url = f"/replays/{game_id}"
    if difficulty_id is not None:
        url += f"?difficulty={difficulty_id}"
    if shot_id is not None:
        url += f"&shot={urllib.parse.quote(shot_id)}"
    if route_id is not None:
        url += f"&route={urllib.parse.quote(route_id)}"
    return url


def convert_replays_to_json_bytes(
    ranked_replays: Iterable[models.Replay],
) -> Iterable[bytes]:
    converter = ReplayToJsonConverter()
    return (converter.convert_replay_to_json_bytes(replay) for replay in ranked_replays)


def _get_medal_emoji(rank: int) -> str:
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    return ""


class _LazyDjangoJSONEncoder(django_json.DjangoJSONEncoder):
    """A JSON encoder that can handle gettext_lazy strings."""

    def default(self, o: Any) -> Any:
        # the _lazy string translation functions return Promises, so force
        # them back to strings.
        if isinstance(o, Promise):
            return str(o)

        return super().default(o)
