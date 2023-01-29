
from django.core import management
from django import test


class MigrateFromCallCommandTestCase(test.TestCase):

    def _CheckDownUp(self, app):
        management.call_command(
            'migrate', app, 'zero', interactive=False
        )
        management.call_command(
            'migrate', app, interactive=False
        )

    def testMigrateDownUp_Users(self):
        self._CheckDownUp('users')

    def testMigrateDownUp_Replays(self):
        self._CheckDownUp('replays')
