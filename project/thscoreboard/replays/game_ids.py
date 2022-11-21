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
            return pgettext('th01', 'Reimu')

    if game_id == GameIDs.TH05:
        if shot_id == 'Reimu':
            return pgettext('th05', 'Reimu')
        if shot_id == 'Marisa':
            return pgettext('th05', 'Marisa')
        if shot_id == 'Mima':
            return pgettext('th05', 'Mima')
        if shot_id == 'Yuuka':
            return pgettext('th05', 'Yuuka')

    if game_id == GameIDs.TH06:
        if shot_id == 'ReimuA':
            return pgettext('th06', 'Reimu A')
        elif shot_id == 'ReimuB':
            return pgettext('th06', 'Reimu B')
        elif shot_id == 'MarisaA':
            return pgettext('th06', 'Marisa A')
        elif shot_id == 'MarisaB':
            return pgettext('th06', 'Marisa B')

    if game_id == GameIDs.TH07:
        if shot_id == 'ReimuA':
            return pgettext('th07', 'Reimu A')
        if shot_id == 'ReimuB':
            return pgettext('th07', 'Reimu B')
        if shot_id == 'MarisaA':
            return pgettext('th07', 'Marisa A')
        if shot_id == 'MarisaB':
            return pgettext('th07', 'Marisa B')
        if shot_id == 'SakuyaA':
            return pgettext('th07', 'Sakuya A')
        if shot_id == 'SakuyaB':
            return pgettext('th07', 'Sakuya B')
        return shot_id

    if game_id == GameIDs.TH10:
        if shot_id == 'ReimuA':
            return pgettext('th10', 'Reimu A')
        elif shot_id == 'ReimuB':
            return pgettext('th10', 'Reimu B')
        elif shot_id == 'ReimuC':
            return pgettext('th10', 'Reimu C')
        elif shot_id == 'MarisaA':
            return pgettext('th10', 'Marisa A')
        elif shot_id == 'MarisaB':
            return pgettext('th10', 'Marisa B')
        elif shot_id == 'MarisaC':
            return pgettext('th10', 'Marisa C')

    if game_id == GameIDs.TH11:
        if shot_id == 'ReimuA':
            return pgettext('th11', 'Reimu A')
        elif shot_id == 'ReimuB':
            return pgettext('th11', 'Reimu B')
        elif shot_id == 'ReimuC':
            return pgettext('th11', 'Reimu C')
        elif shot_id == 'MarisaA':
            return pgettext('th11', 'Marisa A')
        elif shot_id == 'MarisaB':
            return pgettext('th11', 'Marisa B')
        elif shot_id == 'MarisaC':
            return pgettext('th11', 'Marisa C')

    return 'Bug shot'


def GetRouteName(game_id: str, route_id: str):
    if game_id == GameIDs.TH01:
        if route_id == 'Jigoku':
            return pgettext('th01', 'Jigoku')
        elif route_id == 'Makai':
            return pgettext('th01', 'Makai')
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
    if game_id in {GameIDs.TH07}:
        if difficulty == 5:
            return 'Phantasm'
    
    return 'Bug difficulty'
