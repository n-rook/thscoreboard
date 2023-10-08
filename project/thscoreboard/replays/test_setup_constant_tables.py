from django import test
from replays import models
from replays.management.commands.setup_constant_tables import (
    GameConstants,
    create_or_update_games,
)


class CreateOrUpdateGamesTest(test.TestCase):
    def test_creates_games(self):
        test_game_constants = GameConstants(
            id="th00",
            has_replays=True,
            num_difficulties=5,
            shots=["Reimu", "Marisa"],
            routes=["A", "B"],
        )

        create_or_update_games([test_game_constants])

        games_id_db = models.Game.objects.all()
        self.assertEquals(len(games_id_db), 1)

        game_in_db = games_id_db[0]

        self.assertEquals(game_in_db.game_id, test_game_constants.id)
        self.assertEquals(game_in_db.has_replays, test_game_constants.has_replays)
        self.assertEquals(
            game_in_db.num_difficulties, test_game_constants.num_difficulties
        )

        shots_in_db = models.Shot.objects.all()
        self.assertCountEqual(
            (shot.shot_id for shot in shots_in_db), test_game_constants.shots
        )

        for i, route in enumerate(test_game_constants.routes):
            self.assertIsNotNone(
                models.Route.objects.filter(route_id=route, order_number=i).first()
            )

    def test_creates_games_empty_fields(self):
        test_game_constants = GameConstants(
            id="th00",
            has_replays=False,
            num_difficulties=0,
            shots=[],
            routes=[],
        )

        create_or_update_games([test_game_constants])

        games_id_db = models.Game.objects.all()
        self.assertEquals(len(games_id_db), 1)

        game_in_db = games_id_db[0]

        self.assertEquals(game_in_db.game_id, test_game_constants.id)
        self.assertEquals(game_in_db.has_replays, test_game_constants.has_replays)
        self.assertEquals(
            game_in_db.num_difficulties, test_game_constants.num_difficulties
        )

        self.assertEquals(len(models.Shot.objects.all()), 0)
        self.assertEquals(len(models.Route.objects.all()), 0)

    def test_allows_modifying_fields(self):
        test_game_constants = GameConstants(
            id="th00",
            has_replays=False,
            num_difficulties=0,
            shots=[],
            routes=[],
        )

        create_or_update_games([test_game_constants])

        test_game_constants.has_replays = True
        test_game_constants.num_difficulties = 5

        create_or_update_games([test_game_constants])

        games_id_db = models.Game.objects.all()
        self.assertEquals(len(games_id_db), 1)
        game_in_db = games_id_db[0]

        self.assertEquals(game_in_db.has_replays, True)
        self.assertEquals(game_in_db.num_difficulties, 5)

    def test_disallows_modifying_shot_ids(self):
        test_game_constants = GameConstants(
            id="th00",
            has_replays=False,
            num_difficulties=0,
            shots=["Reimu", "Marisa"],
            routes=[],
        )

        create_or_update_games([test_game_constants])

        test_game_constants.shots = ["Reimu", "Marisa", "Cirno"]

        with self.assertRaises(Exception):
            create_or_update_games([test_game_constants])

    def test_disallows_modifying_route_ids(self):
        test_game_constants = GameConstants(
            id="th00",
            has_replays=False,
            num_difficulties=0,
            shots=[],
            routes=["a", "b"],
        )

        create_or_update_games([test_game_constants])

        test_game_constants.routes = ["a", "b", "c"]

        with self.assertRaises(Exception):
            create_or_update_games([test_game_constants])

    def test_disallows_modifying_route_order(self):
        test_game_constants = GameConstants(
            id="th00",
            has_replays=False,
            num_difficulties=0,
            shots=[],
            routes=["a", "b"],
        )

        create_or_update_games([test_game_constants])

        test_game_constants.routes = ["b", "a"]

        with self.assertRaises(Exception):
            create_or_update_games([test_game_constants])
