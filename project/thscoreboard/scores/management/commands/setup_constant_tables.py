import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from scores import models

class Command(BaseCommand):

    help = 'Set up the Game and Shot tables.'

    def handle(self, *args, **kwargs):
        if models.Game.objects.filter(game_id='th06'):
            logging.info('th06 already loaded')
        else:
            _Create06()
            logging.info('Created th06')


@transaction.atomic
def _Create06():
    th06 = models.Game(game_id='th06', has_replays=True)
    th06.save()

    shots = ['ReimuA', 'ReimuB', 'MarisaA', 'MarisaB']
    for shot in shots:
        shot_row = models.Shot(game=th06, shot_id=shot)
        shot_row.save()
