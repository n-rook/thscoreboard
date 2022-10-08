"""Defines generally useful test cases for replay tests."""

from django import test
from django.contrib import auth

from replays.management.commands import setup_constant_tables


class ReplayTestCase(test.TestCase):
    """A test case for database tests in the replays app.

    This test case will set up constant tables for you.
    """

    def setUp(self):
        setup_constant_tables.SetUpConstantTables()
    
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
