from dataclasses import dataclass
from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction
from replays import models


class Command(BaseCommand):
    help = "Set up the Game and Shot tables."

    def handle(self, *args, **kwargs):
        """Set up constant tables in the database."""
        SetUpConstantTables()


def SetUpConstantTables():
    """Set up constant tables in the database.

    In addition to the command, this procedure is available here as a
    separate function, so that tests can call it easily.
    """
    create_or_update_games(all_game_constants)


class InvalidConstantsMutationException(Exception):
    pass


@dataclass
class GameConstants:
    id: str
    has_replays: bool
    num_difficulties: int
    shots: List[str]
    routes: List[str]


th18 = GameConstants(
    id="th18",
    has_replays=True,
    num_difficulties=5,
    shots=["Reimu", "Marisa", "Sakuya", "Sanae"],
    routes=[],
)

th17 = GameConstants(
    id="th17",
    has_replays=True,
    num_difficulties=5,
    shots=[
        "ReimuWolf",
        "ReimuOtter",
        "ReimuEagle",
        "MarisaWolf",
        "MarisaOtter",
        "MarisaEagle",
        "YoumuWolf",
        "YoumuOtter",
        "YoumuEagle",
    ],
    routes=[],
)

th16 = GameConstants(
    id="th16",
    has_replays=True,
    num_difficulties=5,
    shots=[
        "ReimuSpring",
        "ReimuSummer",
        "ReimuAutumn",
        "ReimuWinter",
        "CirnoSpring",
        "CirnoSummer",
        "CirnoAutumn",
        "CirnoWinter",
        "AyaSpring",
        "AyaSummer",
        "AyaAutumn",
        "AyaWinter",
        "MarisaSpring",
        "MarisaSummer",
        "MarisaAutumn",
        "MarisaWinter",
        "Reimu",
        "Cirno",
        "Aya",
        "Marisa",
    ],
    routes=[],
)

th15 = GameConstants(
    id="th15",
    has_replays=True,
    num_difficulties=5,
    shots=["Reimu", "Marisa", "Sanae", "Reisen"],
    routes=[],
)

th14 = GameConstants(
    id="th14",
    has_replays=True,
    num_difficulties=5,
    shots=["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"],
    routes=[],
)

th13 = GameConstants(
    id="th13",
    has_replays=True,
    num_difficulties=5,
    shots=["Reimu", "Marisa", "Sanae", "Youmu"],
    routes=[],
)

th128 = GameConstants(
    id="th128",
    has_replays=True,
    num_difficulties=5,
    shots=["Cirno"],
    routes=[
        "A-1",
        "A-2",
        "B-1",
        "B-2",
        "C-1",
        "C-2",
    ],
)

th12 = GameConstants(
    id="th12",
    has_replays=True,
    num_difficulties=5,
    shots=["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SanaeA", "SanaeB"],
    routes=[],
)

th11 = GameConstants(
    id="th11",
    has_replays=True,
    num_difficulties=5,
    shots=["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"],
    routes=[],
)

th10 = GameConstants(
    id="th10",
    has_replays=True,
    num_difficulties=5,
    shots=["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"],
    routes=[],
)

th09 = GameConstants(
    id="th09",
    has_replays=True,
    num_difficulties=5,
    shots=[
        "Reimu",
        "Marisa",
        "Sakuya",
        "Youmu",
        "Reisen",
        "Cirno",
        "Lyrica",
        "Mystia",
        "Tewi",
        "Yuuka",
        "Aya",
        "Medicine",
        "Komachi",
        "Eiki",
        "Merlin",
        "Lunasa",
    ],
    routes=[],
)

th08 = GameConstants(
    id="th08",
    has_replays=True,
    num_difficulties=5,
    shots=[
        "Reimu & Yukari",
        "Marisa & Alice",
        "Sakuya & Remilia",
        "Youmu & Yuyuko",
        "Reimu",
        "Yukari",
        "Marisa",
        "Alice",
        "Sakuya",
        "Remilia",
        "Youmu",
        "Yuyuko",
    ],
    routes=["Final A", "Final B"],
)

th07 = GameConstants(
    id="th07",
    has_replays=True,
    num_difficulties=6,
    shots=["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"],
    routes=[],
)

th06 = GameConstants(
    id="th06",
    has_replays=True,
    num_difficulties=5,
    shots=["ReimuA", "ReimuB", "MarisaA", "MarisaB"],
    routes=[],
)

th05 = GameConstants(
    id="th05",
    has_replays=False,
    num_difficulties=5,
    shots=["Reimu", "Marisa", "Mima", "Yuuka"],
    routes=[],
)

th04 = GameConstants(
    id="th04",
    has_replays=False,
    num_difficulties=5,
    shots=["ReimuA", "ReimuB", "MarisaA", "MarisaB"],
    routes=[],
)

th03 = GameConstants(
    id="th03",
    has_replays=False,
    num_difficulties=5,
    shots=[
        "Reimu",
        "Mima",
        "Marisa",
        "Ellen",
        "Kotohime",
        "Kana",
        "Rikako",
        "Chiyuri",
        "Yumemi",
    ],
    routes=[],
)

th02 = GameConstants(
    id="th02",
    has_replays=False,
    num_difficulties=5,
    shots=["ReimuA", "ReimuB", "ReimuC"],
    routes=[],
)

th01 = GameConstants(
    id="th01",
    has_replays=False,
    num_difficulties=4,  # No extra in HRtP!
    shots=["Reimu"],
    routes=["Jigoku", "Makai"],
)

all_game_constants = [
    th01,
    th02,
    th03,
    th04,
    th05,
    th06,
    th07,
    th08,
    th09,
    th10,
    th11,
    th12,
    th128,
    th13,
    th14,
    th15,
    th16,
    th17,
    th18,
]


@transaction.atomic
def create_or_update_games(all_game_constants: List[GameConstants]):
    game_rows = models.Game.objects.all()
    for game_row in game_rows:
        if game_row.game_id not in (
            game_constants.id for game_constants in all_game_constants
        ):
            raise InvalidConstantsMutationException(
                f"Found game {game_row.game_id} in database, "
                "but this game is not in the list of game constants."
            )

    for game_constants in all_game_constants:
        game_row = models.Game.objects.filter(game_id=game_constants.id).first()
        if game_row:
            game_row.has_replays = game_constants.has_replays
            game_row.num_difficulties = game_constants.num_difficulties
        else:
            game_row = models.Game(
                game_id=game_constants.id,
                has_replays=game_constants.has_replays,
                num_difficulties=game_constants.num_difficulties,
            )

        create_or_update_shots(game_row, game_constants.shots)
        create_or_update_routes(game_row, game_constants.routes)
        game_row.save()


def create_or_update_shots(game=models.Game, shots=List[str]):
    shot_rows = models.Shot.objects.filter(game=game).all()
    if shot_rows:
        shot_ids_in_db = {shot.shot_id for shot in shot_rows}
        if shot_ids_in_db != set(shots):
            raise InvalidConstantsMutationException(
                "The shots in the constant tables did not match the shots in the db"
            )

    for shot in shots:
        shot_row = models.Shot.objects.filter(shot_id=shot, game=game).first()
        if shot_row is None:
            shot_row = models.Shot(game=game, shot_id=shot)
            shot_row.save()


def create_or_update_routes(game=models.Game, routes=List[str]):
    route_rows = models.Route.objects.filter(game=game).all()
    if route_rows:
        route_ids_in_db = {(route.order_number, route.route_id) for route in route_rows}
        if route_ids_in_db != set(enumerate(routes)):
            raise InvalidConstantsMutationException(
                "The routes in the constant tables did not match the routes in the db"
            )

    for i, route in enumerate(routes):
        route_row = models.Route.objects.filter(route_id=route, game=game).first()
        if route_row is None:
            route_row = models.Route(
                route_id=route, order_number=i, game_id=game.game_id
            )
            route_row.save()
