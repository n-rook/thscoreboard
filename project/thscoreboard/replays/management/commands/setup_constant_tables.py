import logging

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

    _CreateIfNotLoaded("th18", _Create18)
    _CreateIfNotLoaded("th17", _Create17)
    _CreateIfNotLoaded("th16", _Create16)
    _CreateIfNotLoaded("th15", _Create15)
    _CreateIfNotLoaded("th14", _Create14)
    _CreateIfNotLoaded("th13", _Create13)
    _CreateIfNotLoaded("th12", _Create12)
    _CreateIfNotLoaded("th11", _Create11)
    _CreateIfNotLoaded("th10", _Create10)
    _CreateIfNotLoaded("th09", _Create09)
    _CreateIfNotLoaded("th08", _Create08)
    _CreateIfNotLoaded("th07", _Create07)
    _CreateIfNotLoaded("th06", _Create06)
    _CreateIfNotLoaded("th05", _Create05)
    _CreateIfNotLoaded("th04", _Create04)
    _CreateIfNotLoaded("th03", _Create03)
    _CreateIfNotLoaded("th02", _Create02)
    _CreateIfNotLoaded("th01", _Create01)


def _CreateIfNotLoaded(game_id, constant_creation_function):
    if models.Game.objects.filter(game_id=game_id):
        logging.info("%s already loaded", game_id)
    else:
        constant_creation_function()
        logging.info("Created %s", game_id)


@transaction.atomic
def _Create18():
    th18 = models.Game(game_id="th18", has_replays=True, num_difficulties=5)
    th18.save()

    shots = ["Reimu", "Marisa", "Sakuya", "Sanae"]
    for shot in shots:
        shot_row = models.Shot(game=th18, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create17():
    th17 = models.Game(game_id="th17", has_replays=True, num_difficulties=5)
    th17.save()

    shots = [
        "ReimuWolf",
        "ReimuOtter",
        "ReimuEagle",
        "MarisaWolf",
        "MarisaOtter",
        "MarisaEagle",
        "YoumuWolf",
        "YoumuOtter",
        "YoumuEagle",
    ]
    for shot in shots:
        shot_row = models.Shot(game=th17, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create16():
    th16 = models.Game(game_id="th16", has_replays=True, num_difficulties=5)
    th16.save()

    shots = [
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
    ]
    for shot in shots:
        shot_row = models.Shot(game=th16, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create15():
    th15 = models.Game(game_id="th15", has_replays=True, num_difficulties=5)
    th15.save()

    shots = ["Reimu", "Marisa", "Sanae", "Reisen"]
    for shot in shots:
        shot_row = models.Shot(game=th15, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create14():
    th14 = models.Game(game_id="th14", has_replays=True, num_difficulties=5)
    th14.save()

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"]
    for shot in shots:
        shot_row = models.Shot(game=th14, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create13():
    th13 = models.Game(game_id="th13", has_replays=True, num_difficulties=6)
    th13.save()

    shots = ["Reimu", "Marisa", "Sanae", "Youmu"]
    for shot in shots:
        shot_row = models.Shot(game=th13, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create12():
    th12 = models.Game(game_id="th12", has_replays=True, num_difficulties=5)
    th12.save()

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SanaeA", "SanaeB"]
    for shot in shots:
        shot_row = models.Shot(game=th12, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create11():
    th11 = models.Game(game_id="th11", has_replays=True, num_difficulties=5)
    th11.save()

    shots = ["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"]
    for shot in shots:
        shot_row = models.Shot(game=th11, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create10():
    th10 = models.Game(game_id="th10", has_replays=True, num_difficulties=5)
    th10.save()

    shots = ["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"]
    for shot in shots:
        shot_row = models.Shot(game=th10, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create09():
    th09 = models.Game(game_id="th09", has_replays=True, num_difficulties=5)
    th09.save()

    shots = [
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
    ]
    for shot in shots:
        shot_row = models.Shot(game=th09, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create08():
    th08 = models.Game(game_id="th08", has_replays=True, num_difficulties=5)
    th08.save()

    shots = [
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
    ]
    for shot in shots:
        shot_row = models.Shot(game=th08, shot_id=shot)
        shot_row.save()

    routes = ["Final A", "Final B"]
    for i, route_id in enumerate(routes):
        route = models.Route(game=th08, route_id=route_id, order_number=i)
        route.save()


@transaction.atomic
def _Create07():
    th07 = models.Game(game_id="th07", has_replays=True, num_difficulties=6)
    th07.save()

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"]
    for shot in shots:
        shot_row = models.Shot(game=th07, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create06():
    th06 = models.Game(game_id="th06", has_replays=True, num_difficulties=5)
    th06.save()

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]
    for shot in shots:
        shot_row = models.Shot(game=th06, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create05():
    th05 = models.Game(game_id="th05", has_replays=False, num_difficulties=5)
    th05.save()

    shots = ["Reimu", "Marisa", "Mima", "Yuuka"]
    for shot in shots:
        shot_row = models.Shot(game=th05, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create04():
    th04 = models.Game(game_id="th04", has_replays=False, num_difficulties=5)
    th04.save()

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]
    for shot in shots:
        shot_row = models.Shot(game=th04, shot_id=shot)
        shot_row.save()


def _Create03():
    th03 = models.Game(game_id="th03", has_replays=False, num_difficulties=5)
    th03.save()

    shots = [
        "Reimu",
        "Mima",
        "Marisa",
        "Ellen",
        "Kotohime",
        "Kana",
        "Rikako",
        "Chiyuri",
        "Yumemi",
    ]
    for shot in shots:
        shot_row = models.Shot(game=th03, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create02():
    th02 = models.Game(game_id="th02", has_replays=False, num_difficulties=5)
    th02.save()

    shots = ["ReimuA", "ReimuB", "ReimuC"]
    for shot in shots:
        shot_row = models.Shot(game=th02, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create01():
    # No extra in HRtP!
    th01 = models.Game(game_id="th01", has_replays=False, num_difficulties=4)
    th01.save()

    shot = models.Shot(game=th01, shot_id="Reimu")
    shot.save()

    routes = ["Jigoku", "Makai"]
    for i, route_id in enumerate(routes):
        route = models.Route(game=th01, route_id=route_id, order_number=i)
        route.save()
