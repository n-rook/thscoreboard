"""Various human-readable game IDs, used in low-level libraries like game_ids.py."""

from django.utils.translation import gettext as _, pgettext


class GameIDs:
    TH01 = 'th01'
    TH05 = 'th05'
    TH06 = 'th06'
    TH07 = 'th07'
    TH10 = 'th10'
    TH11 = 'th11'


def GetGameName(game_id: str, short=False):
    # Believe it or not, this really is the best way I found to do this.
    # Having the translation strings on different lines makes it so that they
    # are all automatically detected by "makemessages".
    if game_id == GameIDs.TH01:
        if short:
            return _('th01')
        else:
            return _('東方靈異伝 - The Highly Responsive to Prayers')
    if game_id == GameIDs.TH05:
        if short:
            return _('th05')
        else:
            return _('東方怪綺談 - Mystic Square')
    if game_id == GameIDs.TH06:
        if short:
            return _('th06')
        else:
            return _('東方紅魔郷 - Embodiment of Scarlet Devil')
    if game_id == GameIDs.TH07:
        if short:
            return _('th07')
        else:
            return _('東方妖々夢 - Perfect Cherry Blossom')
    if game_id == GameIDs.TH10:
        if short:
            return _('th10')
        else:
            return _('東方風神録 - Mountain of Faith')
    if game_id == GameIDs.TH11:
        if short:
            return _('th11')
        else:
            return _('東方地霊殿 - Subterranean Animism')
    return _('Unknown game (bug!)')


def GetShotName(game_id: str, shot_id: str):
    if game_id == GameIDs.TH01:
        if shot_id == 'Reimu':
            return _('Reimu')
    if game_id == GameIDs.TH05:
        # The names are the same as the short codenames.
        # Well, in English.
        return shot_id
    if game_id == GameIDs.TH06:
        if shot_id == 'ReimuA':
            return 'Reimu A'
        elif shot_id == 'ReimuB':
            return 'Reimu B'
        elif shot_id == 'MarisaA':
            return 'Marisa A'
        elif shot_id == 'MarisaB':
            return 'Marisa B'
    if game_id == GameIDs.TH07:
        return shot_id
    if game_id == GameIDs.TH10:
        if shot_id == 'ReimuA':
            return 'Reimu A (Homing Type)'
        elif shot_id == 'ReimuB':
            return 'Reimu B (Forward Focus Type)'
        elif shot_id == 'ReimuC':
            return 'Reimu C (Sealing Type)'
        elif shot_id == 'MarisaA':
            return 'Marisa A (High-Power Type)'
        elif shot_id == 'MarisaB':
            return 'Marisa B (Piercing Type)'
        elif shot_id == 'MarisaC':
            return 'Marisa C (Magician Type)'
    if game_id == GameIDs.TH11:
        if shot_id == 'ReimuA':
            return 'Reimu A (Yukari Yakumo)'
        elif shot_id == 'ReimuB':
            return 'Reimu B (Suika Ibuki)'
        elif shot_id == 'ReimuC':
            return 'Reimu C (Aya Shameimaru)'
        elif shot_id == 'MarisaA':
            return 'Marisa A (Alice Margatroid)'
        elif shot_id == 'MarisaB':
            return 'Marisa B (Patchouli Knowledge)'
        elif shot_id == 'MarisaC':
            return 'Marisa C (Nitori Kawashiro)'
    return 'Bug shot'


def GetRouteName(game_id: str, route_id: str):
    if game_id == GameIDs.TH01:
        if route_id == 'Jigoku':
            return pgettext('th01 route', 'Jigoku')
        elif route_id == 'Makai':
            return pgettext('th01 route', 'Makai')
    return 'Bug route'


def GetDifficultyName(game_id: str, difficulty: int):
    if game_id in {GameIDs.TH01, GameIDs.TH05, GameIDs.TH06, GameIDs.TH07, GameIDs.TH10, GameIDs.TH11}:
        if difficulty == 0:
            return 'Easy'
        elif difficulty == 1:
            return 'Normal'
        elif difficulty == 2:
            return 'Hard'
        elif difficulty == 3:
            return 'Lunatic'
        elif difficulty == 4:
            return 'Extra'
        elif difficulty == 5:
            return 'Phantasm'
    
    return 'Bug difficulty'
