from django.core.management.base import BaseCommand
from replays.game_ids import GameIDs

import os
import requests


class Command(BaseCommand):
    
    help = 'Download spell names from thpatch.net'

    def handle(self, *args, **kwargs):
        has_thcrap = [GameIDs.TH06, GameIDs.TH07, GameIDs.TH08, GameIDs.TH09, GameIDs.TH10, GameIDs.TH11]
        thcrap_langs = ['en']

        for lang in thcrap_langs:
            for game in has_thcrap:
                os.makedirs(f'replays/spells/{lang}', exist_ok=True)
                with open(f'replays/spells/{lang}/{game}.json', 'wb') as f:
                    f.write(requests.get(f'https://srv.thpatch.net/lang_{lang}/{game}/spells.js').content)
