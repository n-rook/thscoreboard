from django.core.management.base import BaseCommand

import os
import requests
import replays.spell_cards


class Command(BaseCommand):
    
    help = 'Download spell names from thpatch.net'

    def handle(self, *args, **kwargs):

        for lang in replays.spell_cards.thcrap_langs:
            for game in replays.spell_cards.has_spell_practice:
                os.makedirs(f'replays/spells/{lang}', exist_ok=True)
                with open(f'replays/spells/{lang}/{game}.json', 'wb') as f:
                    f.write(requests.get(f'https://srv.thpatch.net/lang_{lang}/{game}/spells.js').content)
