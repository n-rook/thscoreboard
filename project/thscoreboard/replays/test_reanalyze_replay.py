
import datetime

from replays import models
from replays import reanalyze_replay
from replays.testing import test_case
from replays.testing import test_replays


class ReanalyzeReplayTest(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('some-user')

    def GetNew(self, replay):
        """Fetch a new copy of the given replay model."""
        return models.Replay.objects.get(id=replay.id)

    def AssertNoDiff(self, id):
        self.assertEqual(reanalyze_replay.CheckReplay(id), '')
        self.assertFalse(reanalyze_replay.DoesReplayNeedUpdate(id))

    def testNoDiff(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertEqual(diff, '')

    def testNoDiff_Update(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        reanalyze_replay.UpdateReplay(replay.id)
        self.assertEqual(replay, models.Replay.objects.get(id=replay.id))

    def testTimestampDiff(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        replay.timestamp += datetime.timedelta(hours=1)
        replay.save()

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertIn(
            '2018-02-19T10:44:21+00:00 -> 2018-02-19T09:44:21+00:00', diff
        )

    def testTimestampDiff_HasUpdate(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        replay.timestamp += datetime.timedelta(hours=1)
        replay.save()

        self.assertTrue(reanalyze_replay.DoesReplayNeedUpdate(replay.id))

    def testTimestampDiff_Update(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)
        real_timestamp = replay.timestamp

        replay.timestamp += datetime.timedelta(hours=1)
        replay.save()

        reanalyze_replay.UpdateReplay(replay.id)
        new_replay = self.GetNew(replay)

        self.assertEqual(real_timestamp, new_replay.timestamp)
        self.AssertNoDiff(replay.id)

    def testStage2Diff(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        stage2 = models.ReplayStage.objects.get(replay=replay, stage=1)
        stage2.piv += 100000
        stage2.save()

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertIn('Stage 2:', diff)
        self.assertIn(
            '[piv] 259660 -> 159660', diff
        )

    def testStage2Diff_HasUpdate(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        stage2 = models.ReplayStage.objects.get(replay=replay, stage=1)
        stage2.piv += 100000
        stage2.save()

        self.assertTrue(reanalyze_replay.DoesReplayNeedUpdate(replay.id))

    def testStage2Diff_Update(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        stage2 = models.ReplayStage.objects.get(replay=replay, stage=1)
        stage2_piv = stage2.piv
        stage2.piv += 100000
        stage2.save()

        reanalyze_replay.UpdateReplay(replay.id)
        new_stage2 = models.ReplayStage.objects.get(replay=replay, stage=1)
        self.assertEqual(new_stage2.stage, 1)
        self.assertEqual(stage2_piv, new_stage2.piv)

        self.AssertNoDiff(replay.id)

    def testStage2Missing(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        stage2 = models.ReplayStage.objects.get(replay=replay, stage=1)
        stage2.delete()

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertIn('Stage 2:', diff)
        self.assertIn(
            '[piv] (No model!) -> 159660', diff
        )

    def testStage2Missing_HasUpdate(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        stage2 = models.ReplayStage.objects.get(replay=replay, stage=1)
        stage2.delete()

        self.assertTrue(reanalyze_replay.DoesReplayNeedUpdate(replay.id))

    def testStage2Missing_Update(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        old_stages = list(models.ReplayStage.objects.filter(replay=replay).order_by('stage'))
        stage2 = old_stages[1]
        self.assertEqual(stage2.stage, 1)
        stage2_piv = stage2.piv
        stage2.delete()

        reanalyze_replay.UpdateReplay(replay.id)
        new_stages = models.ReplayStage.objects.filter(replay=replay).order_by('stage')
        self.assertEqual(len(new_stages), 6)
        self.assertEqual(new_stages[1].stage, 1)
        self.assertEqual(new_stages[1].piv, stage2_piv)

        self.AssertNoDiff(replay.id)

    def testStage9_HasUpdate(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        fake_stage_9 = models.ReplayStage(replay=replay, stage=8, piv=999999)
        fake_stage_9.save()

        self.assertTrue(reanalyze_replay.DoesReplayNeedUpdate(replay.id))

    def testStage9(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        fake_stage_9 = models.ReplayStage(replay=replay, stage=8, piv=999999)
        fake_stage_9.save()

        diff = reanalyze_replay.CheckReplay(replay.id)
        self.assertIn('Stage 9:', diff)
        self.assertIn('[piv] 999999 -> (No model!)', diff)

    def testStage9_Update(self):
        replay = test_replays.CreateAsPublishedReplay('th10_normal', self.user)

        fake_stage_9 = models.ReplayStage(replay=replay, stage=8, piv=999999)
        fake_stage_9.save()

        reanalyze_replay.UpdateReplay(replay.id)
        with self.assertRaises(models.ReplayStage.DoesNotExist):
            models.ReplayStage.objects.get(replay=replay, stage=9)

    def testTH08(self):
        # Regression test for https://github.com/n-rook/thscoreboard/issues/244
        replay = test_replays.CreateAsPublishedReplay('th8_normal', self.user)
        self.assertFalse(reanalyze_replay.DoesReplayNeedUpdate(replay.id))
