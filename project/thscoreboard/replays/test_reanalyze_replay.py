
import datetime

from replays import models
from replays import reanalyze_replay
from replays.testing import test_case
from replays.testing import test_replays


class ReanalyzeReplayTest(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('some-user')

    def testNoDiff(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertEqual(diff, '')

    def testTimestampDiff(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        replay.timestamp += datetime.timedelta(hours=1)
        replay.save()

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertIn(
            '2018-02-19T10:44:21+00:00 -> 2018-02-19T09:44:21+00:00', diff
        )

    def testStage2Diff(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        stage2 = models.ReplayStage.objects.get(replay=replay, stage=1)
        stage2.piv += 100000
        stage2.save()

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertIn('Stage 1:', diff)
        self.assertIn(
            '[piv] 214270 -> 114270', diff
        )

    def testStage2Missing(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        stage2 = models.ReplayStage.objects.get(replay=replay, stage=1)
        stage2.delete()

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertIn('Stage 1:', diff)
        self.assertIn(
            '[piv] (No model!) -> 114270', diff
        )

    def testStage9(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        fake_stage_9 = models.ReplayStage(replay=replay, stage=8, piv=999999)
        fake_stage_9.save()

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertIn('Stage 8:', diff)
        self.assertIn('[piv] 999999 -> (No model!)', diff)
