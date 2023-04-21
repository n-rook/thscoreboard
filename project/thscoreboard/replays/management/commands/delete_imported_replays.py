import logging
from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Q

from replays import models


class Command(BaseCommand):
    help = """Delete all imported replays. These are identified by the fact that
    their imported username is not None.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        super().add_arguments(parser)

    def handle(self, *args, **options):
        delete_imported_replays()


def delete_imported_replays() -> None:
    deleted_count, _ = models.Replay.objects.filter(~Q(imported_username=None)).delete()
    logging.info("Deleted %d replays", deleted_count)
