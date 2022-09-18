"""Defines generally useful test cases for replay tests."""

from django import test

from replays.management.commands import setup_constant_tables


class ReplayTestCase(test.TestCase):
    """A test case for database tests in the replays app.

    This test case will set up constant tables for you.
    """

    def setUp(self):
        setup_constant_tables.SetUpConstantTables()
