
import datetime

from replays import models
from replays.testing import test_case
from replays.testing import test_replays

REPLAY_1 = test_replays.GetRaw('th6_extra')
REPLAY_2 = test_replays.GetRaw('th10_normal')


class TemporaryReplayFileTest(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('somebody')

    def testCleanUpDoesNothingWithNoReplays(self):

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        models.TemporaryReplayFile.CleanUp(now)

    def testCleanUpDeletesOldReplaysButNotNewOnes(self):

        now = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)

        delete_me = models.TemporaryReplayFile(
            user=self.user,
            replay=REPLAY_1,
            created=now - datetime.timedelta(days=32)
        )
        delete_me.save()

        dont_delete_me = models.TemporaryReplayFile(
            user=self.user,
            replay=REPLAY_2,
            created=now - datetime.timedelta(days=28)
        )
        dont_delete_me.save()

        models.TemporaryReplayFile.CleanUp(now)

        with self.assertRaises(models.TemporaryReplayFile.DoesNotExist):
            models.TemporaryReplayFile.objects.get(id=delete_me.id)
        
        models.TemporaryReplayFile.objects.get(id=dont_delete_me.id)
        # No exception; it does exist.
