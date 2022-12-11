"""Various human-readable game IDs, used in low-level libraries like game_ids.py."""

from django.utils.translation import gettext as _, pgettext


class GameIDs:
    TH01 = 'th01'
    TH02 = 'th02'
    TH03 = 'th03'
    TH04 = 'th04'
    TH05 = 'th05'
    TH06 = 'th06'
    TH07 = 'th07'
    TH08 = 'th08'
    TH09 = 'th09'
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
    if game_id == GameIDs.TH02:
        if short:
            return _('th02')
        else:
            return _('東方封魔録 - Story of Eastern Wonderland')
    if game_id == GameIDs.TH03:
        if short:
            return _('th03')
        else:
            return _('東方夢時空 - The Phantasmagoria of Dim. Dream')
    if game_id == GameIDs.TH04:
        if short:
            return _('th04')
        else:
            return _('東方幻想郷 - Lotus Land Story')
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
    if game_id == GameIDs.TH08:
        if short:
            return _('th08')
        else:
            return _('東方永夜抄 - Imperishable Night')
    if game_id == GameIDs.TH09:
        if short:
            return _('th09')
        else:
            return _('東方花映塚 - Phantasmagoria of Flower View')
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
    if game_id == GameIDs.TH02:
        if shot_id == 'ReimuA':
            return pgettext('th02', 'Mobility')
        elif shot_id == 'ReimuB':
            return pgettext('th02', 'Defensive')
        elif shot_id == 'ReimuC':
            return pgettext('th02', 'Offensive')

    if game_id == GameIDs.TH03:
        if shot_id == 'Reimu':
            return pgettext('th03', 'Reimu')
        elif shot_id == 'Mima':
            return pgettext('th03', 'Mima')
        elif shot_id == 'Marisa':
            return pgettext('th03', 'Marisa')
        elif shot_id == 'Ellen':
            return pgettext('th03', 'Ellen')
        elif shot_id == 'Kotohime':
            return pgettext('th03', 'Kotohime')
        elif shot_id == 'Kana':
            return pgettext('th03', 'Kana')
        elif shot_id == 'Rikako':
            return pgettext('th03', 'Rikako')
        elif shot_id == 'Chiyuri':
            return pgettext('th03', 'Chiyuri')
        elif shot_id == 'Yumemi':
            return pgettext('th03', 'Yumemi')

    if game_id == GameIDs.TH04:
        if shot_id == 'ReimuA':
            return pgettext('th04', 'Reimu A')
        elif shot_id == 'ReimuB':
            return pgettext('th04', 'Reimu B')
        elif shot_id == 'MarisaA':
            return pgettext('th04', 'Marisa A')
        elif shot_id == 'MarisaB':
            return pgettext('th04', 'Marisa B')

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

    if game_id == GameIDs.TH08:
        if shot_id == 'Reimu & Yukari':
            return pgettext('th08', 'Reimu & Yukari')
        if shot_id == 'Marisa & Alice':
            return pgettext('th08', 'Marisa & Alice')
        if shot_id == 'Sakuya & Remilia':
            return pgettext('th08', 'Sakuya & Remilia')
        if shot_id == 'Youmu & Yuyuko':
            return pgettext('th08', 'Youmu & Yuyuko')
        if shot_id == 'Reimu':
            return pgettext('th08', 'Reimu')
        if shot_id == 'Yukari':
            return pgettext('th08', 'Yukari')
        if shot_id == 'Marisa':
            return pgettext('th08', 'Marisa')
        if shot_id == 'Alice':
            return pgettext('th08', 'Alice')
        if shot_id == 'Sakuya':
            return pgettext('th08', 'Sakuya')
        if shot_id == 'Remilia':
            return pgettext('th08', 'Remilia')
        if shot_id == 'Youmu':
            return pgettext('th08', 'Youmu')
        if shot_id == 'Yuyuko':
            return pgettext('th08', 'Yuyuko')
        return shot_id

    if game_id == GameIDs.TH09:
        if shot_id == "Reimu":
            return pgettext('th09', "Reimu",)
        if shot_id == "Marisa":
            return pgettext('th09', "Marisa",)
        if shot_id == "Sakuya":
            return pgettext('th09', "Sakuya",)
        if shot_id == "Youmu":
            return pgettext('th09', "Youmu",)
        if shot_id == "Reisen":
            return pgettext('th09', "Reisen",)
        if shot_id == "Cirno":
            return pgettext('th09', "Cirno",)
        if shot_id == "Lyrica":
            return pgettext('th09', "Lyrica",)
        if shot_id == "Mystia":
            return pgettext('th09', "Mystia",)
        if shot_id == "Tewi":
            return pgettext('th09', "Tewi",)
        if shot_id == "Yuuka":
            return pgettext('th09', "Yuuka",)
        if shot_id == "Aya":
            return pgettext('th09', "Aya",)
        if shot_id == "Medicine":
            return pgettext('th09', "Medicine",)
        if shot_id == "Komachi":
            return pgettext('th09', "Komachi",)
        if shot_id == "Eiki":
            return pgettext('th09', "Eiki",)
        if shot_id == "Merlin":
            return pgettext('th09', "Merlin",)
        if shot_id == "Lunasa":
            return pgettext('th09', "Lunasa")
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
    if game_id == GameIDs.TH08:
        if route_id == 'Final A':
            return pgettext('th08', 'Final A')
        elif route_id == 'Final B':
            return pgettext('th08', 'Final B')
    return 'Bug route'


def GetDifficultyName(game_id: str, difficulty: int):
    if game_id in {
            GameIDs.TH01,
            GameIDs.TH02,
            GameIDs.TH03,
            GameIDs.TH04,
            GameIDs.TH05,
            GameIDs.TH06,
            GameIDs.TH07,
            GameIDs.TH08,
            GameIDs.TH09,
            GameIDs.TH10,
            GameIDs.TH11}:
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
