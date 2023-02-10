
import datetime

from django import test
from django.db import utils
from django.db.models import deletion
from django.utils import timezone

from replays import models as replay_models
from replays.testing import test_case
from replays.testing import test_replays
from users import models


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


class RegistrationTestCase(test_case.UserTestCase):

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

    def testBannedUnverifiedUser(self):
        unverified_user = models.UnverifiedUser.CreateUser(
            'banned-username',
            'some-email@example.com',
            'some-password',
        )

        now = datetime.datetime.now(datetime.timezone.utc)
        ban = models.Ban(
            author=self.createUser('banner'),
            reason='something',
            expiration=now + datetime.timedelta(minutes=15),
            duration=datetime.timedelta(minutes=15),
            target=None,
            deleted_account_username='banned-username',
            deleted_account_email='email@example.com'
        )
        ban.save()

        with self.assertRaises(models.BannedError):
            unverified_user.VerifyUser()

    def testBannedUnverifiedEmail(self):
        unverified_user = models.UnverifiedUser.CreateUser(
            'some-username',
            'banned@example.com',
            'some-password',
        )

        now = datetime.datetime.now(datetime.timezone.utc)
        ban = models.Ban(
            author=self.createUser('banner'),
            reason='something',
            expiration=now + datetime.timedelta(minutes=15),
            duration=datetime.timedelta(minutes=15),
            target=None,
            deleted_account_username='blah-blah',
            deleted_account_email='banned@example.com'
        )
        ban.save()

        with self.assertRaises(models.BannedError):
            unverified_user.VerifyUser()

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


class BanTestCase(test_case.UserTestCase):

    def setUp(self):
        super().setUp()

        self.banner = self.createUser('banner')
        self.target = self.createUser('target')

        self.now = datetime.datetime.now(datetime.timezone.utc)

    def testNotBanned(self):
        self.assertFalse(self.target.CheckIfBanned())

    def testBanUser(self):
        b = self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now
        )
        self.assertEqual(b.author, self.banner)
        self.assertEqual(b.target, self.target)
        self.assertEqual(b.reason, 'test')
        self.assertEqual(b.duration, datetime.timedelta(hours=6))
        self.assertAlmostEqual(b.expiration, self.now, delta=datetime.timedelta(minutes=1))

        self.assertEqual(b, models.Ban.objects.filter(target=self.target).get())

        self.assertEqual(self.target.might_be_banned, True)

    def testBanUserComputesExpirationTime(self):
        b = self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6)
        )
        self.assertAlmostEqual(
            b.expiration,
            self.now + datetime.timedelta(hours=6),
            delta=datetime.timedelta(minutes=1))

    def testBanned(self):
        self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now + datetime.timedelta(hours=3)
        )
        self.assertTrue(self.target.CheckIfBanned())

    def testBanExpired(self):
        self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now - datetime.timedelta(hours=3)
        )
        self.assertFalse(self.target.CheckIfBanned())

        updated_target = models.User.objects.get(id=self.target.id)
        self.assertFalse(updated_target.might_be_banned)

    def testCannotDirectlyDeleteBannedUser(self):
        self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now + datetime.timedelta(hours=3)
        )
        with self.assertRaises(deletion.ProtectedError):
            self.target.delete()

    def testCleanUpBannedUserSetsSecondaryFields(self):
        b = self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now + datetime.timedelta(hours=3)
        )

        self.target.MarkForDeletion()
        self.target.deleted_on -= datetime.timedelta(days=180)
        self.target.save()

        models.User.CleanUp(self.now)

        b = models.Ban.objects.get(id=b.id)
        self.assertIsNone(b.target)
        self.assertEquals('target', b.deleted_account_username)
        self.assertEquals(self.target.email, b.deleted_account_email)

    def testCleanUpBannedUser_IsXBanned(self):
        target_email = self.target.email

        self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now + datetime.timedelta(hours=3)
        )

        self.assertFalse(models.Ban.IsUsernameBanned('target'))
        self.assertFalse(models.Ban.IsEmailBanned(target_email))

        self.target.MarkForDeletion()
        self.target.deleted_on -= datetime.timedelta(days=180)
        self.target.save()

        models.User.CleanUp(self.now)

        self.assertTrue(models.Ban.IsUsernameBanned('target'))
        self.assertTrue(models.Ban.IsEmailBanned(target_email))

    def testCleanUpBannedUser_IsXBannedRespectExpirationTime(self):
        target_email = self.target.email

        self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now + datetime.timedelta(hours=3)
        )
        self.target.MarkForDeletion()
        self.target.deleted_on -= datetime.timedelta(days=180)
        self.target.save()
        models.User.CleanUp(self.now)

        self.assertTrue(models.Ban.IsUsernameBanned('target'))
        self.assertTrue(models.Ban.IsEmailBanned(target_email))

        self.assertFalse(models.Ban.IsUsernameBanned('target', now=self.now + datetime.timedelta(days=3)))
        self.assertFalse(models.Ban.IsEmailBanned(target_email, now=self.now + datetime.timedelta(days=3)))

    def testCleanUpBan_NotDeleted(self):
        b = self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now - datetime.timedelta(days=90)
        )

        models.Ban.CleanUp(self.now)
        self.assertTrue(models.Ban.objects.filter(id=b.id).exists())

    def testCleanUpBan_NotExpired(self):
        b = self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now + datetime.timedelta(days=90)
        )
        self.target.MarkForDeletion()
        self.target.deleted_on -= datetime.timedelta(days=180)
        self.target.save()
        models.User.CleanUp(self.now)

        models.Ban.CleanUp(self.now)
        self.assertTrue(models.Ban.objects.filter(id=b.id).exists())

    def testCleanUpBan_RecentlyExpired(self):
        b = self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now - datetime.timedelta(days=5)
        )
        self.target.MarkForDeletion()
        self.target.deleted_on -= datetime.timedelta(days=180)
        self.target.save()
        models.User.CleanUp(self.now)

        models.Ban.CleanUp(self.now)
        self.assertTrue(models.Ban.objects.filter(id=b.id).exists())

    def testCleanUpBan_LongExpired(self):
        b = self.target.BanUser(
            self.banner,
            'test',
            datetime.timedelta(hours=6),
            expiration=self.now - datetime.timedelta(days=90)
        )
        self.target.MarkForDeletion()
        self.target.deleted_on -= datetime.timedelta(days=180)
        self.target.save()
        models.User.CleanUp(self.now)

        models.Ban.CleanUp(self.now)
        self.assertFalse(models.Ban.objects.filter(id=b.id).exists())


class DeletedUserTest(test_case.UserTestCase):

    def setUp(self):
        super().setUp()

        self.user = self.createUser('some-user')
        self.now = datetime.datetime.now(datetime.timezone.utc)

    def testMarkForDeletion(self):
        self.user.MarkForDeletion()
        self.assertFalse(self.user.is_active)
        self.assertAlmostEqual(
            self.user.deleted_on,
            self.now,
            delta=datetime.timedelta(minutes=1)
        )

    def testCannotSetDeletedOnForActiveUser(self):
        self.user.deleted_on = self.now
        with self.assertRaises(utils.IntegrityError):
            self.user.save()

    def testCannotMakeUserInactiveWithoutDeletedOn(self):
        self.user.is_active = False
        with self.assertRaises(utils.IntegrityError):
            self.user.save()

    def testCleanUpDeletesMarkedUsers(self):
        self.user.delete()  # not used in this test.

        long_deleted_user = self.createUser('long-deleted-user')
        long_deleted_user.MarkForDeletion()
        long_deleted_user = models.User.objects.get(username='long-deleted-user')
        long_deleted_user.deleted_on = self.now - datetime.timedelta(days=75)
        long_deleted_user.save()

        recently_deleted_user = self.createUser('recently-deleted-user')
        recently_deleted_user.MarkForDeletion()
        recently_deleted_user = models.User.objects.get(username='recently-deleted-user')
        recently_deleted_user.deleted_on = self.now - datetime.timedelta(days=15)
        recently_deleted_user.save()

        _ = self.createUser('active-user')

        models.User.CleanUp(self.now)

        usernames = {u.username for u in models.User.objects.all()}
        self.assertEqual(usernames, {'recently-deleted-user', 'active-user'})


class DeleteAnAccountWithReplaysTestCase(test_case.ReplayTestCase):

    def testDeleteAnAccountWithAReplay(self):
        u = self.createUser('doomed')
        now = datetime.datetime.now(datetime.timezone.utc)

        r = test_replays.CreateAsPublishedReplay(
            filename='th6_extra',
            user=u
        )

        models.Visits.RecordVisit(
            user=u,
            ip='127.0.0.1'
        )

        u.MarkForDeletion()
        u.deleted_on -= datetime.timedelta(days=90)
        u.save()

        models.User.CleanUp(now)

        self.assertFalse(models.User.objects.filter(id=u.id).exists())
        self.assertFalse(replay_models.Replay.objects.filter(id=r.id).exists())
        self.assertFalse(models.Visits.objects.filter(ip='127.0.0.1').exists())
