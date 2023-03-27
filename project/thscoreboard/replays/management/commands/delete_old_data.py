from django.core.management.base import BaseCommand
from django.utils import timezone
from replays import models as replay_models
from users import models as user_models


class Command(BaseCommand):
    help = "Delete expired temporary data."

    def handle(self, *args, **kwargs):
        """Delete expired temporary data."""
        _DeleteExpiredTemporaryData()


def _DeleteExpiredTemporaryData():
    # Don't do this in a transaction; it's a heavy operation, and it's still
    # useful even if interrupted halfway.

    now = timezone.now()

    replay_models.TemporaryReplayFile.CleanUp(now)
    user_models.UnverifiedUser.CleanUp(now)
    user_models.InvitedUser.CleanUp(now)
    user_models.Visits.CleanUp(now)
    user_models.User.CleanUp(now)
    user_models.Ban.CleanUp(now)
