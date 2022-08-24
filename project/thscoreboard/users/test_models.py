from django import test

from . import models


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
