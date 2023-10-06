import itertools

from replays import game_ids
from replays import models
from replays import get_all_games
from replays import create_replay
from replays import replay_parsing
from replays import constant_helpers
from replays.testing import test_case
from replays.testing import test_replays


class ReplayTest(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()

    def testGetByCategoryReturnsAllGamesExactlyOnce(self):
        all_games = models.Game.objects.all()
        all_games_by_category = get_all_games.get_all_games_by_category()
        games_from_categories = itertools.chain.from_iterable(
            all_games_by_category.values()
        )
        self.assertCountEqual(
            (g.game_id for g in all_games),
            (g.game_id for g in games_from_categories),
        )
