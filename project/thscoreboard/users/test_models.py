
import datetime

from django import test
from django.utils import timezone

from replays.testing import test_case
from . import models


class InviteTestCase(test.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self._staff = models.User.objects.create_superuser(
            username='root',
            email='root@example.com',
            password='root',
        )

    def testInviteUser(self):
        invite = models.InvitedUser.CreateInvite(
            'some-username',
            'some-email@example.com',
            self._staff
        )
        self.assertTrue(invite.token)
        self.assertEqual(
            invite,
            models.InvitedUser.objects.get(token=invite.token),
        )

        invite.AcceptInvite('some-password')

        with self.assertRaises(models.InvitedUser.DoesNotExist):
            models.InvitedUser.objects.get(token=invite.token)

        real_user = models.User.objects.get(username='some-username')
        self.assertTrue(
            real_user.check_password('some-password')
        )


class RegistrationTestCase(test.TestCase):

    def testUnverifiedUser(self):
        unverified_user = models.UnverifiedUser.CreateUser(
            'some-username',
            'some-email@example.com',
            'some-password',
        )

        self.assertTrue(unverified_user.token)
        unverified_user_from_db = models.UnverifiedUser.objects.get(
            token=unverified_user.token)

        self.assertEqual(unverified_user, unverified_user_from_db)

        unverified_user_from_db.VerifyUser()

        with self.assertRaises(models.UnverifiedUser.DoesNotExist):
            models.UnverifiedUser.objects.get(token=unverified_user.token)

        real_user = models.User.objects.get(username='some-username')
        self.assertTrue(
            real_user.check_password('some-password')
        )

    def testUnverifiedUserCleanUp_DeletesExpectedUsers(self):
        now = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)

        delete_me = models.UnverifiedUser.CreateUser(
            'user1',
            'user1@example.com',
            'some-password',
        )
        delete_me.created = now - datetime.timedelta(days=32)
        delete_me.save()

        dont_delete_me = models.UnverifiedUser.CreateUser(
            'user2',
            'user2@example.com',
            'some-password',
        )
        dont_delete_me.created = now - datetime.timedelta(days=28)
        dont_delete_me.save()

        models.UnverifiedUser.CleanUp(now)

        with self.assertRaises(models.UnverifiedUser.DoesNotExist):
            models.UnverifiedUser.objects.get(id=delete_me.id)

        models.UnverifiedUser.objects.get(id=dont_delete_me.id)
        # Does not fail.


class VisitsTestCase(test_case.UserTestCase):

    def testRecordVisit(self):
        u = self.createUser('somebody')
        models.Visits.RecordVisit(u, '1.2.3.4')

        models.Visits.objects.filter(user=u, ip='1.2.3.4').get()
        # No error.

    def testRecordVisit_RecordsTimestamp(self):
        u = self.createUser('somebody')
        models.Visits.RecordVisit(u, '1.2.3.4')

        v = models.Visits.objects.filter(user=u, ip='1.2.3.4').get()
        self.assertLess(v.created, timezone.now())
        self.assertGreater(v.created, timezone.now() - datetime.timedelta(seconds=15))

    def testRecordAnonymousVisit(self):
        models.Visits.RecordVisit(None, '1.2.3.4')

        models.Visits.objects.filter(user=None, ip='1.2.3.4').get()
        # No error.

    def testDoesNotRecordDuplicates(self):
        u = self.createUser('somebody')
        for _ in range(10):
            models.Visits.RecordVisit(u, '1.2.3.4')

        visit_count = models.Visits.objects.filter(user=u, ip='1.2.3.4').count()
        self.assertEqual(visit_count, 1)
