"""Defines generally useful test cases for replay tests."""

from django import test
from django.contrib import auth

from replays.management.commands import setup_constant_tables


class UserTestCase(test.TestCase):
    """A test case for database tests.

    This test case contains some utility methods that are useful when
    testing users.
    """

    def createUser(self, username):
        """Creates a user for tests."""
        User = auth.get_user_model()
        u = User(
            username=User.normalize_username(username),
            email=User.normalize_email(f'{username}@example.com'),
            password='password'
        )
        u.save()
        return u


class ReplayTestCase(UserTestCase):
    """A test case for database tests in the replays app.

    This test case will set up constant tables for you. It also contains
    the utility methods in UserTestCase.
    """

    def setUp(self):
        setup_constant_tables.SetUpConstantTables()
