import logging

from django.core.management.base import BaseCommand
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
            
        if models.Game.objects.filter(game_id='th05'):
            logging.info('th05 already loaded')
        else:
            _Create05()
            logging.info('Created th05')


@transaction.atomic
def _Create06():
    th06 = models.Game(game_id='th06', has_replays=True, num_difficulties=5)
    th06.save()

    shots = ['ReimuA', 'ReimuB', 'MarisaA', 'MarisaB']
    for shot in shots:
        shot_row = models.Shot(game=th06, shot_id=shot)
        shot_row.save()


@transaction.atomic
def _Create05():
    th05 = models.Game(game_id='th05', has_replays=False, num_difficulties=5)
    th05.save()

    shots = ['Reimu', 'Marisa', 'Mima', 'Yuuka']
    for shot in shots:
        shot_row = models.Shot(game=th05, shot_id=shot)
        shot_row.save()
