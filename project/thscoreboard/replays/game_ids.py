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
    TH12 = 'th12'
    TH13 = 'th13'
    TH14 = 'th14'
    TH15 = 'th15'
    TH16 = 'th16'
    TH17 = 'th17'
    TH18 = 'th18'


class ReplayTypes:
    REGULAR = 1
    STAGE_PRACTICE = 2
    SPELL_PRACTICE = 3
    PVP = 4


def GetReplayType(r_type: int):
    if r_type == 1:
        return _('Regular')
    elif r_type == 2:
        return _('Stage Practice')
    elif r_type == 3:
        return _('Spell Practice')
    elif r_type == 4:
        return _('PVP')
    return 'Bug type'


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
    if game_id == GameIDs.TH12:
        if short:
            return _('th12')
        else:
            return _('東方星蓮船 - Undefined Fantastic Object')
    if game_id == GameIDs.TH13:
        if short:
            return _('th13')
        else:
            return _('東方神霊廟 - Ten Desires')
    if game_id == GameIDs.TH14:
        if short:
            return _('th14')
        else:
            return _('東方輝針城 - Double Dealing Character')
    if game_id == GameIDs.TH15:
        if short:
            return _('th15')
        else:
            return _('東方紺珠伝 - Legacy of Lunatic Kingdom')
    if game_id == GameIDs.TH16:
        if short:
            return _('th16')
        else:
            return _('東方天空璋 - Hidden Star in Four Seasons')
    if game_id == GameIDs.TH17:
        if short:
            return _('th17')
        else:
            return _('東方鬼形獣 - Wily Beast and Weakest Creature')
    if game_id == GameIDs.TH18:
        if short:
            return _('th18')
        else:
            return _('東方虹龍洞 - Unconnected Marketeers')
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

    if game_id == GameIDs.TH12:
        if shot_id == 'ReimuA':
            return pgettext('th12', 'Reimu A')
        elif shot_id == 'ReimuB':
            return pgettext('th12', 'Reimu B')
        elif shot_id == 'MarisaA':
            return pgettext('th12', 'Marisa A')
        elif shot_id == 'MarisaB':
            return pgettext('th12', 'Marisa B')
        elif shot_id == 'SanaeA':
            return pgettext('th12', 'Sanae A')
        elif shot_id == 'SanaeB':
            return pgettext('th12', 'Sanae B')

    if game_id == GameIDs.TH13:
        if shot_id == 'Reimu':
            return pgettext('th13', 'Reimu')
        elif shot_id == 'Marisa':
            return pgettext('th13', 'Marisa')
        elif shot_id == 'Sanae':
            return pgettext('th13', 'Sanae')
        elif shot_id == 'Youmu':
            return pgettext('th13', 'Youmu')

    if game_id == GameIDs.TH14:
        if shot_id == "ReimuA":
            return pgettext('th14', "ReimuA")
        elif shot_id == "ReimuB":
            return pgettext('th14', "ReimuB")
        elif shot_id == "MarisaA":
            return pgettext('th14', "MarisaA")
        elif shot_id == "MarisaB":
            return pgettext('th14', "MarisaB")
        elif shot_id == "SakuyaA":
            return pgettext('th14', "SakuyaA")
        elif shot_id == "SakuyaB":
            return pgettext('th14', "SakuyaB")

    if game_id == GameIDs.TH15:
        if shot_id == "Reimu":
            return pgettext('th15', "Reimu")
        elif shot_id == "Marisa":
            return pgettext('th15', "Marisa")
        elif shot_id == "Sanae":
            return pgettext('th15', "Sanae")
        elif shot_id == "Reisen":
            return pgettext('th15', "Reisen")

    if game_id == GameIDs.TH16:
        if shot_id == "Reimu":
            return pgettext('th16', "Reimu")
        elif shot_id == "ReimuSpring":
            return pgettext('th16', "Reimu Spring")
        elif shot_id == "ReimuSummer":
            return pgettext('th16', "Reimu Summer")
        elif shot_id == "ReimuAutumn":
            return pgettext('th16', "Reimu Autumn")
        elif shot_id == "ReimuWinter":
            return pgettext('th16', "Reimu Winter")
        elif shot_id == "Cirno":
            return pgettext('th16', "Cirno")
        elif shot_id == "CirnoSpring":
            return pgettext('th16', "Cirno Spring")
        elif shot_id == "CirnoSummer":
            return pgettext('th16', "Cirno Summer")
        elif shot_id == "CirnoAutumn":
            return pgettext('th16', "Cirno Autumn")
        elif shot_id == "CirnoWinter":
            return pgettext('th16', "Cirno Winter")
        elif shot_id == "Aya":
            return pgettext('th16', "Aya")
        elif shot_id == "AyaSpring":
            return pgettext('th16', "Aya Spring")
        elif shot_id == "AyaSummer":
            return pgettext('th16', "Aya Summer")
        elif shot_id == "AyaAutumn":
            return pgettext('th16', "Aya Autumn")
        elif shot_id == "AyaWinter":
            return pgettext('th16', "Aya Winter")
        elif shot_id == "Marisa":
            return pgettext('th16', "Marisa")
        elif shot_id == "MarisaSpring":
            return pgettext('th16', "Marisa Spring")
        elif shot_id == "MarisaSummer":
            return pgettext('th16', "Marisa Summer")
        elif shot_id == "MarisaAutumn":
            return pgettext('th16', "Marisa Autumn")
        elif shot_id == "MarisaWinter":
            return pgettext('th16', "Marisa Winter")

    if game_id == GameIDs.TH17:
        if shot_id == 'ReimuWolf':
            return pgettext('th17', 'Reimu Wolf')
        elif shot_id == 'ReimuOtter':
            return pgettext('th17', 'Reimu Otter')
        elif shot_id == 'ReimuEagle':
            return pgettext('th17', 'Reimu Eagle')
        elif shot_id == 'MarisaWolf':
            return pgettext('th17', 'Marisa Wolf')
        elif shot_id == 'MarisaOtter':
            return pgettext('th17', 'Marisa Otter')
        elif shot_id == 'MarisaEagle':
            return pgettext('th17', 'Marisa Eagle')
        elif shot_id == 'YoumuWolf':
            return pgettext('th17', 'Youmu Wolf')
        elif shot_id == 'YoumuOtter':
            return pgettext('th17', 'Youmu Otter')
        elif shot_id == 'YoumuEagle':
            return pgettext('th17', 'Youmu Eagle')

    if game_id == GameIDs.TH18:
        if shot_id == "Reimu":
            return pgettext('th18', "Reimu")
        elif shot_id == "Marisa":
            return pgettext('th18', "Marisa")
        elif shot_id == "Sakuya":
            return pgettext('th18', "Sakuya")
        elif shot_id == "Sanae":
            return pgettext('th18', "Sanae")
        
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
            GameIDs.TH11,
            GameIDs.TH12,
            GameIDs.TH13,
            GameIDs.TH14,
            GameIDs.TH15,
            GameIDs.TH16,
            GameIDs.TH17,
            GameIDs.TH18,
    }:
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
    if game_id in {GameIDs.TH13}:
        if difficulty == 5:
            return 'Overdrive'

    return 'Bug difficulty'
