"""Various human-readable game IDs, used in low-level libraries like game_ids.py."""

import enum
from typing import Optional

from immutabledict import immutabledict

from django.utils.translation import gettext as _, pgettext


class GameIDs:
    TH01 = "th01"
    TH02 = "th02"
    TH03 = "th03"
    TH04 = "th04"
    TH05 = "th05"
    TH06 = "th06"
    TH07 = "th07"
    TH08 = "th08"
    TH09 = "th09"
    TH10 = "th10"
    TH11 = "th11"
    TH12 = "th12"
    TH13 = "th13"
    TH14 = "th14"
    TH15 = "th15"
    TH16 = "th16"
    TH17 = "th17"
    TH18 = "th18"


class ReplayTypes:
    REGULAR = 1
    STAGE_PRACTICE = 2
    SPELL_PRACTICE = 3
    PVP = 4


def GetReplayType(r_type: int):
    if r_type == 1:
        return _("Regular")
    elif r_type == 2:
        return _("Stage Practice")
    elif r_type == 3:
        return _("Spell Practice")
    elif r_type == 4:
        return _("PVP")
    return "Bug type"


class NameLength(enum.Enum):
    SHORT = 0
    """A short name for a game, like "EoSD"."""
    STANDARD = 1
    """A moderate-length name, like "Embodiment of Scarlet Devil"."""
    FULL = 2
    """The full-length name, like "東方紅魔郷 - Embodiment of Scarlet Devil"."""


# Believe it or not, this really is the best way I found to do this.
# Having the translation strings on different lines makes it so that they
# are all automatically detected by "makemessages".
_GAME_NAMES = immutabledict(
    {
        GameIDs.TH01: (
            pgettext("short game name", "th01"),
            pgettext("standard game name", "The Highly Responsive to Prayers"),
            pgettext("full game name", "東方靈異伝 - The Highly Responsive to Prayers"),
        ),
        GameIDs.TH02: (
            pgettext("short game name", "th02"),
            pgettext("standard game name", "Story of Eastern Wonderland"),
            pgettext("full game name", "東方封魔録 - Story of Eastern Wonderland"),
        ),
        GameIDs.TH03: (
            pgettext("short game name", "th03"),
            pgettext("standard game name", "The Phantasmagoria of Dim. Dream"),
            pgettext("full game name", "東方夢時空 - The Phantasmagoria of Dim. Dream"),
        ),
        GameIDs.TH04: (
            pgettext("short game name", "th04"),
            pgettext("standard game name", "Lotus Land Story"),
            pgettext("full game name", "東方幻想郷 - Lotus Land Story"),
        ),
        GameIDs.TH05: (
            pgettext("short game name", "th05"),
            pgettext("standard game name", "Mystic Square"),
            pgettext("full game name", "東方怪綺談 - Mystic Square"),
        ),
        GameIDs.TH06: (
            pgettext("short game name", "th06"),
            pgettext("standard game name", "Embodiment of Scarlet Devil"),
            pgettext("full game name", "東方紅魔郷 - Embodiment of Scarlet Devil"),
        ),
        GameIDs.TH07: (
            pgettext("short game name", "th07"),
            pgettext("standard game name", "Perfect Cherry Blossom"),
            pgettext("full game name", "東方妖々夢 - Perfect Cherry Blossom"),
        ),
        GameIDs.TH08: (
            pgettext("short game name", "th08"),
            pgettext("standard game name", "Imperishable Night"),
            pgettext("full game name", "東方永夜抄 - Imperishable Night"),
        ),
        GameIDs.TH09: (
            pgettext("short game name", "th09"),
            pgettext("standard game name", "Phantasmagoria of Flower View"),
            pgettext("full game name", "東方花映塚 - Phantasmagoria of Flower View"),
        ),
        GameIDs.TH10: (
            pgettext("short game name", "th10"),
            pgettext("standard game name", "Mountain of Faith"),
            pgettext("full game name", "東方風神録 - Mountain of Faith"),
        ),
        GameIDs.TH11: (
            pgettext("short game name", "th11"),
            pgettext("standard game name", "Subterranean Animism"),
            pgettext("full game name", "東方地霊殿 - Subterranean Animism"),
        ),
        GameIDs.TH12: (
            pgettext("short game name", "th12"),
            pgettext("standard game name", "Undefined Fantastic Object"),
            pgettext("full game name", "東方星蓮船 - Undefined Fantastic Object"),
        ),
        GameIDs.TH13: (
            pgettext("short game name", "th13"),
            pgettext("standard game name", "Ten Desires"),
            pgettext("full game name", "東方神霊廟 - Ten Desires"),
        ),
        GameIDs.TH14: (
            pgettext("short game name", "th14"),
            pgettext("standard game name", "Double Dealing Character"),
            pgettext("full game name", "東方輝針城 - Double Dealing Character"),
        ),
        GameIDs.TH15: (
            pgettext("short game name", "th15"),
            pgettext("standard game name", "Legacy of Lunatic Kingdom"),
            pgettext("full game name", "東方紺珠伝 - Legacy of Lunatic Kingdom"),
        ),
        GameIDs.TH16: (
            pgettext("short game name", "th16"),
            pgettext("standard game name", "Hidden Star in Four Seasons"),
            pgettext("full game name", "東方天空璋 - Hidden Star in Four Seasons"),
        ),
        GameIDs.TH17: (
            pgettext("short game name", "th17"),
            pgettext("standard game name", "Wily Beast and Weakest Creature"),
            pgettext("full game name", "東方鬼形獣 - Wily Beast and Weakest Creature"),
        ),
        GameIDs.TH18: (
            pgettext("short game name", "th18"),
            pgettext("standard game name", "Unconnected Marketeers"),
            pgettext("full game name", "東方虹龍洞 - Unconnected Marketeers"),
        ),
    }
)


def GetGameName(game_id: str, name_length: NameLength):
    if game_id in _GAME_NAMES:
        return _GAME_NAMES[game_id][name_length.value]
    return _("Unknown game (bug!)")


def GetShotName(game_id: str, shot_id: str) -> str:
    if game_id == GameIDs.TH01:
        if shot_id == "Reimu":
            return pgettext("th01", "Reimu")
    if game_id == GameIDs.TH02:
        if shot_id == "ReimuA":
            return pgettext("th02", "Mobility")
        elif shot_id == "ReimuB":
            return pgettext("th02", "Defensive")
        elif shot_id == "ReimuC":
            return pgettext("th02", "Offensive")

    if game_id == GameIDs.TH03:
        if shot_id == "Reimu":
            return pgettext("th03", "Reimu")
        elif shot_id == "Mima":
            return pgettext("th03", "Mima")
        elif shot_id == "Marisa":
            return pgettext("th03", "Marisa")
        elif shot_id == "Ellen":
            return pgettext("th03", "Ellen")
        elif shot_id == "Kotohime":
            return pgettext("th03", "Kotohime")
        elif shot_id == "Kana":
            return pgettext("th03", "Kana")
        elif shot_id == "Rikako":
            return pgettext("th03", "Rikako")
        elif shot_id == "Chiyuri":
            return pgettext("th03", "Chiyuri")
        elif shot_id == "Yumemi":
            return pgettext("th03", "Yumemi")

    if game_id == GameIDs.TH04:
        if shot_id == "ReimuA":
            return pgettext("th04", "Reimu A")
        elif shot_id == "ReimuB":
            return pgettext("th04", "Reimu B")
        elif shot_id == "MarisaA":
            return pgettext("th04", "Marisa A")
        elif shot_id == "MarisaB":
            return pgettext("th04", "Marisa B")

    if game_id == GameIDs.TH05:
        if shot_id == "Reimu":
            return pgettext("th05", "Reimu")
        if shot_id == "Marisa":
            return pgettext("th05", "Marisa")
        if shot_id == "Mima":
            return pgettext("th05", "Mima")
        if shot_id == "Yuuka":
            return pgettext("th05", "Yuuka")

    if game_id == GameIDs.TH06:
        if shot_id == "ReimuA":
            return pgettext("th06", "Reimu A")
        elif shot_id == "ReimuB":
            return pgettext("th06", "Reimu B")
        elif shot_id == "MarisaA":
            return pgettext("th06", "Marisa A")
        elif shot_id == "MarisaB":
            return pgettext("th06", "Marisa B")

    if game_id == GameIDs.TH07:
        if shot_id == "ReimuA":
            return pgettext("th07", "Reimu A")
        if shot_id == "ReimuB":
            return pgettext("th07", "Reimu B")
        if shot_id == "MarisaA":
            return pgettext("th07", "Marisa A")
        if shot_id == "MarisaB":
            return pgettext("th07", "Marisa B")
        if shot_id == "SakuyaA":
            return pgettext("th07", "Sakuya A")
        if shot_id == "SakuyaB":
            return pgettext("th07", "Sakuya B")
        return shot_id

    if game_id == GameIDs.TH08:
        if shot_id == "Reimu & Yukari":
            return pgettext("th08", "Reimu & Yukari")
        if shot_id == "Marisa & Alice":
            return pgettext("th08", "Marisa & Alice")
        if shot_id == "Sakuya & Remilia":
            return pgettext("th08", "Sakuya & Remilia")
        if shot_id == "Youmu & Yuyuko":
            return pgettext("th08", "Youmu & Yuyuko")
        if shot_id == "Reimu":
            return pgettext("th08", "Reimu")
        if shot_id == "Yukari":
            return pgettext("th08", "Yukari")
        if shot_id == "Marisa":
            return pgettext("th08", "Marisa")
        if shot_id == "Alice":
            return pgettext("th08", "Alice")
        if shot_id == "Sakuya":
            return pgettext("th08", "Sakuya")
        if shot_id == "Remilia":
            return pgettext("th08", "Remilia")
        if shot_id == "Youmu":
            return pgettext("th08", "Youmu")
        if shot_id == "Yuyuko":
            return pgettext("th08", "Yuyuko")
        return shot_id

    if game_id == GameIDs.TH09:
        if shot_id == "Reimu":
            return pgettext(
                "th09",
                "Reimu",
            )
        if shot_id == "Marisa":
            return pgettext(
                "th09",
                "Marisa",
            )
        if shot_id == "Sakuya":
            return pgettext(
                "th09",
                "Sakuya",
            )
        if shot_id == "Youmu":
            return pgettext(
                "th09",
                "Youmu",
            )
        if shot_id == "Reisen":
            return pgettext(
                "th09",
                "Reisen",
            )
        if shot_id == "Cirno":
            return pgettext(
                "th09",
                "Cirno",
            )
        if shot_id == "Lyrica":
            return pgettext(
                "th09",
                "Lyrica",
            )
        if shot_id == "Mystia":
            return pgettext(
                "th09",
                "Mystia",
            )
        if shot_id == "Tewi":
            return pgettext(
                "th09",
                "Tewi",
            )
        if shot_id == "Yuuka":
            return pgettext(
                "th09",
                "Yuuka",
            )
        if shot_id == "Aya":
            return pgettext(
                "th09",
                "Aya",
            )
        if shot_id == "Medicine":
            return pgettext(
                "th09",
                "Medicine",
            )
        if shot_id == "Komachi":
            return pgettext(
                "th09",
                "Komachi",
            )
        if shot_id == "Eiki":
            return pgettext(
                "th09",
                "Eiki",
            )
        if shot_id == "Merlin":
            return pgettext(
                "th09",
                "Merlin",
            )
        if shot_id == "Lunasa":
            return pgettext("th09", "Lunasa")
        return shot_id

    if game_id == GameIDs.TH10:
        if shot_id == "ReimuA":
            return pgettext("th10", "Reimu A")
        elif shot_id == "ReimuB":
            return pgettext("th10", "Reimu B")
        elif shot_id == "ReimuC":
            return pgettext("th10", "Reimu C")
        elif shot_id == "MarisaA":
            return pgettext("th10", "Marisa A")
        elif shot_id == "MarisaB":
            return pgettext("th10", "Marisa B")
        elif shot_id == "MarisaC":
            return pgettext("th10", "Marisa C")

    if game_id == GameIDs.TH11:
        if shot_id == "ReimuA":
            return pgettext("th11", "Reimu A")
        elif shot_id == "ReimuB":
            return pgettext("th11", "Reimu B")
        elif shot_id == "ReimuC":
            return pgettext("th11", "Reimu C")
        elif shot_id == "MarisaA":
            return pgettext("th11", "Marisa A")
        elif shot_id == "MarisaB":
            return pgettext("th11", "Marisa B")
        elif shot_id == "MarisaC":
            return pgettext("th11", "Marisa C")

    if game_id == GameIDs.TH12:
        if shot_id == "ReimuA":
            return pgettext("th12", "Reimu A")
        elif shot_id == "ReimuB":
            return pgettext("th12", "Reimu B")
        elif shot_id == "MarisaA":
            return pgettext("th12", "Marisa A")
        elif shot_id == "MarisaB":
            return pgettext("th12", "Marisa B")
        elif shot_id == "SanaeA":
            return pgettext("th12", "Sanae A")
        elif shot_id == "SanaeB":
            return pgettext("th12", "Sanae B")

    if game_id == GameIDs.TH13:
        if shot_id == "Reimu":
            return pgettext("th13", "Reimu")
        elif shot_id == "Marisa":
            return pgettext("th13", "Marisa")
        elif shot_id == "Sanae":
            return pgettext("th13", "Sanae")
        elif shot_id == "Youmu":
            return pgettext("th13", "Youmu")

    if game_id == GameIDs.TH14:
        if shot_id == "ReimuA":
            return pgettext("th14", "Reimu A")
        elif shot_id == "ReimuB":
            return pgettext("th14", "Reimu B")
        elif shot_id == "MarisaA":
            return pgettext("th14", "Marisa A")
        elif shot_id == "MarisaB":
            return pgettext("th14", "Marisa B")
        elif shot_id == "SakuyaA":
            return pgettext("th14", "Sakuya A")
        elif shot_id == "SakuyaB":
            return pgettext("th14", "Sakuya B")

    if game_id == GameIDs.TH15:
        if shot_id == "Reimu":
            return pgettext("th15", "Reimu")
        elif shot_id == "Marisa":
            return pgettext("th15", "Marisa")
        elif shot_id == "Sanae":
            return pgettext("th15", "Sanae")
        elif shot_id == "Reisen":
            return pgettext("th15", "Reisen")

    if game_id == GameIDs.TH16:
        if shot_id == "Reimu":
            return pgettext("th16", "Reimu")
        elif shot_id == "ReimuSpring":
            return pgettext("th16", "Reimu Spring")
        elif shot_id == "ReimuSummer":
            return pgettext("th16", "Reimu Summer")
        elif shot_id == "ReimuAutumn":
            return pgettext("th16", "Reimu Autumn")
        elif shot_id == "ReimuWinter":
            return pgettext("th16", "Reimu Winter")
        elif shot_id == "Cirno":
            return pgettext("th16", "Cirno")
        elif shot_id == "CirnoSpring":
            return pgettext("th16", "Cirno Spring")
        elif shot_id == "CirnoSummer":
            return pgettext("th16", "Cirno Summer")
        elif shot_id == "CirnoAutumn":
            return pgettext("th16", "Cirno Autumn")
        elif shot_id == "CirnoWinter":
            return pgettext("th16", "Cirno Winter")
        elif shot_id == "Aya":
            return pgettext("th16", "Aya")
        elif shot_id == "AyaSpring":
            return pgettext("th16", "Aya Spring")
        elif shot_id == "AyaSummer":
            return pgettext("th16", "Aya Summer")
        elif shot_id == "AyaAutumn":
            return pgettext("th16", "Aya Autumn")
        elif shot_id == "AyaWinter":
            return pgettext("th16", "Aya Winter")
        elif shot_id == "Marisa":
            return pgettext("th16", "Marisa")
        elif shot_id == "MarisaSpring":
            return pgettext("th16", "Marisa Spring")
        elif shot_id == "MarisaSummer":
            return pgettext("th16", "Marisa Summer")
        elif shot_id == "MarisaAutumn":
            return pgettext("th16", "Marisa Autumn")
        elif shot_id == "MarisaWinter":
            return pgettext("th16", "Marisa Winter")

    if game_id == GameIDs.TH17:
        if shot_id == "ReimuWolf":
            return pgettext("th17", "Reimu Wolf")
        elif shot_id == "ReimuOtter":
            return pgettext("th17", "Reimu Otter")
        elif shot_id == "ReimuEagle":
            return pgettext("th17", "Reimu Eagle")
        elif shot_id == "MarisaWolf":
            return pgettext("th17", "Marisa Wolf")
        elif shot_id == "MarisaOtter":
            return pgettext("th17", "Marisa Otter")
        elif shot_id == "MarisaEagle":
            return pgettext("th17", "Marisa Eagle")
        elif shot_id == "YoumuWolf":
            return pgettext("th17", "Youmu Wolf")
        elif shot_id == "YoumuOtter":
            return pgettext("th17", "Youmu Otter")
        elif shot_id == "YoumuEagle":
            return pgettext("th17", "Youmu Eagle")

    if game_id == GameIDs.TH18:
        if shot_id == "Reimu":
            return pgettext("th18", "Reimu")
        elif shot_id == "Marisa":
            return pgettext("th18", "Marisa")
        elif shot_id == "Sakuya":
            return pgettext("th18", "Sakuya")
        elif shot_id == "Sanae":
            return pgettext("th18", "Sanae")

    return "Bug shot"


def GetCharacterName(game_id: str, shot_id: str) -> str:
    if game_id == GameIDs.TH16:
        if shot_id.startswith("Reimu"):
            return pgettext("th16", "Reimu")
        elif shot_id.startswith("Cirno"):
            return pgettext("th16", "Cirno")
        elif shot_id.startswith("Aya"):
            return pgettext("th16", "Aya")
        elif shot_id.startswith("Marisa"):
            return pgettext("th16", "Marisa")
    if game_id == GameIDs.TH17:
        if shot_id.startswith("Reimu"):
            return pgettext("th17", "Reimu")
        elif shot_id.startswith("Marisa"):
            return pgettext("th17", "Marisa")
        elif shot_id.startswith("Youmu"):
            return pgettext("th17", "Youmu")

    return "Character name not implemented"


def GetSubshotName(game_id: str, shot_id: str) -> Optional[str]:
    if game_id == GameIDs.TH16:
        if shot_id.endswith("Spring"):
            return pgettext("th16", "Spring")
        elif shot_id.endswith("Summer"):
            return pgettext("th16", "Summer")
        elif shot_id.endswith("Autumn"):
            return pgettext("th16", "Autumn")
        elif shot_id.endswith("Winter"):
            return pgettext("th16", "Winter")
        else:
            return None
    if game_id == GameIDs.TH17:
        if shot_id.endswith("Wolf"):
            return pgettext("th16", "Wolf")
        elif shot_id.endswith("Otter"):
            return pgettext("th16", "Otter")
        elif shot_id.endswith("Eagle"):
            return pgettext("th16", "Eagle")

    return "Subshot not implemented"


def GetRouteName(game_id: str, route_id: str):
    if game_id == GameIDs.TH01:
        if route_id == "Jigoku":
            return pgettext("th01", "Jigoku")
        elif route_id == "Makai":
            return pgettext("th01", "Makai")
    if game_id == GameIDs.TH08:
        if route_id == "Final A":
            return pgettext("th08", "Final A")
        elif route_id == "Final B":
            return pgettext("th08", "Final B")
    return "Bug route"


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
            return "Easy"
        elif difficulty == 1:
            return "Normal"
        elif difficulty == 2:
            return "Hard"
        elif difficulty == 3:
            return "Lunatic"
        elif difficulty == 4:
            return "Extra"
    if game_id in {GameIDs.TH07}:
        if difficulty == 5:
            return "Phantasm"
    if game_id in {GameIDs.TH13}:
        if difficulty == 5:
            return "Overdrive"

    return "Bug difficulty"


def GetRpyGameCode(game_id: str) -> str:
    if game_id == GameIDs.TH06:
        return "th6"
    elif game_id == GameIDs.TH07:
        return "th7"
    elif game_id == GameIDs.TH08:
        return "th8"
    elif game_id == GameIDs.TH09:
        return "th9"
    else:
        return game_id


def MakeBase36ReplayId(id: int) -> str:
    base36 = "0123456789abcdefghijklmnopqrstuvwxyz"
    digits = ""
    while id:
        digits += base36[id % len(base36)]
        id //= len(base36)
    return digits[::-1].zfill(4)


def HasBombs(game_id: str, replay_type: Optional[int] = None) -> bool:
    """Returns whether we track bomb usage for a given game and mode.

    Args:
        game_id: The game.
        replay_type: The type of replay. If unset, this function returns True
            if any replay type (for the given game) has bombs.
    """
    if game_id == GameIDs.TH09:
        # PoFV does not have traditional bombs.
        return False

    if replay_type == ReplayTypes.SPELL_PRACTICE:
        # In most cases, you cannot bomb in spell practice.
        # In rare cases, you can (for example, in TH16 you can get a score
        # extend, allowing you to die and then bomb), but even then, it is
        # not worth tracking.
        return False

    return True


def HasLives(game_id: str, replay_type: Optional[int] = None) -> bool:
    """Returns whether we track misses for a given game and mode.

    Args:
        game_id: The game.
        replay_type: The type of replay. If unset, this function returns True
            if we should track misses for any replay type (for the given game).
    """

    # All currently supported games have lives, but scene games don't, so in
    # the future we will return False sometimes here.
    del game_id  # Stop flake8 from complaining that it is unused.

    if replay_type == ReplayTypes.SPELL_PRACTICE:
        # In most cases, you cannot bomb in spell practice.
        # In rare cases, you can (for example, in TH16 you can get a score
        # extend, allowing you to die and then bomb), but even then, it is
        # not worth tracking.
        return False

    return True
