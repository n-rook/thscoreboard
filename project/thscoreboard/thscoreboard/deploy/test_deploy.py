from django.core import management
from django import test


class MigrateFromCallCommandTestCase(test.TestCase):
    def _CheckDownUp(self, app):
        management.call_command("migrate", app, "zero", interactive=False, verbosity=0)
        management.call_command("migrate", app, interactive=False, verbosity=0)

    def testMigrateDownUp_Users(self):
        self._CheckDownUp("users")

    def testMigrateDownUp_Replays(self):
        self._CheckDownUp("replays")


class ModelsMatchMigrationsTestCase(test.TestCase):
    def testModelsMatchMigrations(self):
        # Raise an error if migration files need to be created.
        management.call_command(
            "makemigrations",
            "--check",
            "--noinput",
            "--dry-run",
            "--traceback",
            verbosity=0,
        )
