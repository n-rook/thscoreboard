from unittest.mock import patch

from replays.rank_replays import add_global_rank_annotations
from replays.testing import test_case
from replays import models
from replays.testing import test_replays


class GlobalRankAnnotationsTestCase(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("some-user")

    def _create_n_replays(self, n: int, is_tas: bool = False) -> None:
        with patch("replays.constant_helpers.CalculateReplayFileHash") as mocked_hash:
            for i in range(n):
                mocked_hash.return_value = bytes(i)
                test_replays.CreateAsPublishedReplay(
                    "th10_normal",
                    user=self.user,
                    score=1_000_000_000 - 100_000_000 * i,
                    difficulty=0,
                    category=(
                        models.Category.TAS if is_tas else models.Category.STANDARD
                    ),
                )

    def testRanksAgainstAllReplays(self):
        self._create_n_replays(3)
        replay_subset = models.Replay.objects.order_by("-score")[1:]
        add_global_rank_annotations(replay_subset)

        self.assertEqual(replay_subset[0].rank, 2)
        self.assertEqual(replay_subset[1].rank, 3)

    def testGivesNegativeRankToReplaysOutsideTopThree(self):
        self._create_n_replays(5)
        replay_subset = models.Replay.objects.order_by("-score")[3:]
        add_global_rank_annotations(replay_subset)

        self.assertEqual(replay_subset[0].rank, -1)
        self.assertEqual(replay_subset[1].rank, -1)

    def testIgnoresUnrankedGlobalReplays(self):
        self._create_n_replays(3, is_tas=True)
        test_replays.CreateAsPublishedReplay(
            "th10_normal", user=self.user, score=0, difficulty=0
        )
        replay_subset = models.Replay.objects.order_by("-score")[3:]
        add_global_rank_annotations(replay_subset)

        self.assertEqual(replay_subset[0].rank, 1)
