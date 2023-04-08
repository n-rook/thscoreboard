import dataclasses
from typing import List, Optional
import datetime
from kaitaistruct import KaitaiStructError

from replays.lib import time
from . import game_ids
from .kaitai_parsers import th06
from .kaitai_parsers import th07
from .kaitai_parsers import th08
from .kaitai_parsers import th09
from .kaitai_parsers import th10
from .kaitai_parsers import th11
from .kaitai_parsers import th12
from .kaitai_parsers import th13
from .kaitai_parsers import th14
from .kaitai_parsers import th15
from .kaitai_parsers import th16
from .kaitai_parsers import th17
from .kaitai_parsers import th18
from .kaitai_parsers import th_modern
from .kaitai_parsers import th08_userdata

import math
import logging
import tsadecode as td


class Error(Exception):
    pass


class BadReplayError(Error):
    pass


class UnsupportedGameError(Error):
    pass


class UnsupportedReplayError(Error):
    pass


# when adding new fields, they must be appended to the bottom regardless of the order you'd actually like them to be in
#   otherwise python throws a fit, there's probably a good reason but I don't know it
@dataclasses.dataclass
class ReplayStage:
    stage: int = None
    score: int = None
    piv: int = None
    graze: int = None
    point_items: int = None
    power: int = None
    lives: Optional[int] = None
    life_pieces: Optional[int] = None
    bombs: Optional[int] = None
    bomb_pieces: Optional[int] = None
    th06_rank: int = None
    th07_cherry: int = None
    th07_cherrymax: int = None
    th09_p1_cpu: bool = None
    th09_p2_cpu: bool = None
    th09_p2_shot: str = None
    th09_p2_score: int = None
    th13_trance: int = None
    extends: int = None
    th16_season_power: int = None

    def __getitem__(self, item):
        return getattr(self, item)


@dataclasses.dataclass
class ReplayInfo:
    game: str
    shot: str
    difficulty: int
    score: int
    timestamp: datetime.datetime
    """The timestamp for the replay.

    This field is an aware datetime.
    """

    name: str
    replay_type: int
    route: Optional[str] = None
    spell_card_id: Optional[int] = None
    stages: List[ReplayStage] = dataclasses.field(default_factory=list)
    slowdown: Optional[float] = None

    @property
    def spell_card_id_format(self):
        """Get frontend formatted spellcard id (1-indexed instead of 0-indexed)"""
        return self.spell_card_id + 1

    def __post_init__(self):
        if self.timestamp.tzinfo is None:
            # Why require the datetime be aware?
            # Basically, it's because Python timezone handling is a disaster.
            # datetimes without explicit timezone info tend to be converted
            # in weird ways by builtin methods, so it's way too easy to
            # accidentally apply a timezone correction twice.
            raise ValueError("timestamp datetime must be aware")


# piv is stored with extra precision, we trunctate the value to what is shown ingame
def convert_stored_PIV_to_displayed(game_id: str, piv: int) -> int:
    if game_id in ["th12", "th13", "th14", "th15", "th16", "th17", "th18"]:
        return (math.trunc(piv / 1000)) * 10
    return piv


def _Parse06(rep_raw):
    cryptdata = bytearray(rep_raw[15:])
    td.decrypt06(cryptdata, rep_raw[14])
    replay = th06.Th06.from_bytes(cryptdata)

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]

    rep_stages = []

    enumerated_non_dummy_stages = [
        (i, _stage)
        for i, _stage in enumerate(replay.stages)
        if replay.file_header.stage_offsets[i] != 0
    ]
    # TH06 stores stage data values from the start of the stage but score from the end
    for (i, current_stage), (j, next_stage) in zip(
        enumerated_non_dummy_stages, enumerated_non_dummy_stages[1:] + [(None, None)]
    ):
        s = ReplayStage(stage=i + 1, score=current_stage.score)
        if next_stage is not None:
            s.power = next_stage.power
            s.lives = next_stage.lives
            s.bombs = next_stage.bombs
            s.th06_rank = next_stage.rank

        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and rep_raw[7] != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH06,
        shot=shots[rep_raw[6]],
        difficulty=rep_raw[7],
        score=replay.file_header.score,
        timestamp=time.strptime(replay.file_header.date, "%m/%d/%y"),
        name=replay.file_header.name.replace("\x00", ""),
        slowdown=replay.file_header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse07(rep_raw):
    comp_data = bytearray(rep_raw[16:])
    td.decrypt06(comp_data, rep_raw[13])
    #   please don't ask what is going on here
    #   0x54 - 16 = 68

    comp_size = int.from_bytes(comp_data[4:8], byteorder="little")
    replay = th07.Th07.from_bytes(
        bytearray(rep_raw[0:16])
        + comp_data[0:68]
        + td.unlzss(comp_data[68 : 68 + comp_size])
    )

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"]

    rep_stages = []

    enumerated_non_dummy_stages = [
        (i, _stage)
        for i, _stage in enumerate(replay.stages)
        if replay.file_header.stage_offsets[i] != 0
    ]

    def is_phantasm(difficulty_code: int) -> bool:
        return difficulty_code == 5

    # TH07 stores stage data values from the start of the stage but score from the end
    for (i, current_stage), (j, next_stage) in zip(
        enumerated_non_dummy_stages, enumerated_non_dummy_stages[1:] + [(None, None)]
    ):
        s = ReplayStage(
            stage=i + 2 if is_phantasm(replay.header.difficulty) else i + 1,
            score=current_stage.score * 10,
        )
        if next_stage is not None:
            s.power = next_stage.power
            s.piv = next_stage.piv
            s.lives = next_stage.lives
            s.bombs = next_stage.bombs
            s.graze = next_stage.graze
            s.point_items = next_stage.point_items
            s.th07_cherry = next_stage.cherry
            s.th07_cherrymax = next_stage.cherrymax

        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty not in [4, 5]:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH07,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=time.strptime(replay.header.date, "%m/%d"),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse08(rep_raw):
    comp_data_size = int.from_bytes(rep_raw[12:16], byteorder="little") - 24
    comp_data = bytearray(rep_raw[24:comp_data_size])

    #   read the userdata section to use the date for later
    #   th08_userdata is a modified version of thmodern adapted to ZUN's early userdata format
    user = th08_userdata.Th08Userdata.from_bytes(rep_raw)

    td.decrypt06(comp_data, rep_raw[21])
    #   basically copied from _Parse07()
    #   0x68 (104) - 24 = 80
    replay = th08.Th08.from_bytes(
        bytearray(rep_raw[0:24]) + comp_data[0:80] + td.unlzss(comp_data[80:])
    )

    shots = [
        "Reimu & Yukari",
        "Marisa & Alice",
        "Sakuya & Remilia",
        "Youmu & Yuyuko",
        "Reimu",
        "Yukari",
        "Marisa",
        "Alice",
        "Sakuya",
        "Remilia",
        "Youmu",
        "Yuyuko",
    ]

    rep_stages = []

    if replay.header.spell_card_id != 65535:  # FF FF
        #   spell practice, so stage info isn't necessary
        return ReplayInfo(
            game=game_ids.GameIDs.TH08,
            shot=shots[replay.header.shot],
            difficulty=replay.header.difficulty,
            score=replay.header.score * 10,
            timestamp=time.strptime(user.userdata.date.value, "%Y/%m/%d %H:%M:%S"),
            name=replay.header.name.replace("\x00", ""),
            slowdown=replay.header.slowdown,
            replay_type=game_ids.ReplayTypes.SPELL_PRACTICE,
            spell_card_id=replay.header.spell_card_id,
        )

    #   else regular run

    # TH08 stores stage data values from the start of the stage but score from the end
    route = None
    enumerated_non_dummy_stages = [
        (i, _stage)
        for i, _stage in enumerate(replay.stages)
        if replay.file_header.stage_offsets[i] != 0
    ]
    for (i, current_stage), (j, next_stage) in zip(
        enumerated_non_dummy_stages, enumerated_non_dummy_stages[1:] + [(None, None)]
    ):
        s = ReplayStage(
            stage=i + 1,
            score=current_stage.score * 10,
        )
        if next_stage is not None:
            s.power = next_stage.power
            s.piv = next_stage.piv
            s.lives = next_stage.lives
            s.bombs = next_stage.bombs
            s.graze = next_stage.graze
            s.point_items = next_stage.point_items

        if i == 6:
            route = "Final A"
        elif i == 7:
            route = "Final B"

        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH08,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=time.strptime(user.userdata.date.value, "%Y/%m/%d %H:%M:%S"),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        route=route,
        stages=rep_stages,
    )

    return r


def _Parse09(rep_raw):
    comp_data_size = int.from_bytes(rep_raw[12:16], byteorder="little") - 24
    comp_data = bytearray(rep_raw[24:comp_data_size])
    td.decrypt06(comp_data, rep_raw[21])
    #   0xc0 (192) - 24 = 168
    replay = th09.Th09.from_bytes(
        bytearray(rep_raw[0:24]) + comp_data[0:168] + td.unlzss(comp_data[168:])
    )
    shots = [
        "Reimu",
        "Marisa",
        "Sakuya",
        "Youmu",
        "Reisen",
        "Cirno",
        "Lyrica",
        "Mystia",
        "Tewi",
        "Yuuka",
        "Aya",
        "Medicine",
        "Komachi",
        "Eiki",
        "Merlin",
        "Lunasa",
    ]

    rep_stages = []
    r_score = 0
    r_shot = "Bug shot"
    r_type = game_ids.ReplayTypes.REGULAR

    highest_stage = 0
    if replay.file_header.stage_offsets[9] == 0:
        #  story mode
        #  collect start-of-stage data
        for i in range(9):
            if replay.file_header.stage_offsets[i] != 0:
                #   real stage
                p1 = replay.stages[i]
                p2 = replay.stages[i + 10]

                s = ReplayStage()
                s.stage = i + 1
                s.score = p1.score * 10
                s.lives = p1.lives

                s.th09_p1_cpu = False
                s.th09_p2_cpu = True
                s.th09_p2_shot = shots[p2.shot]
                s.th09_p2_score = p2.score * 10

                highest_stage = i
                rep_stages.append(s)

            #  fill in replayinfo
            p1 = replay.stages[highest_stage]
            r_shot = shots[p1.shot]
            r_score = p1.score * 10

        #  adjust stage data to be end-of-stage by shuffling them down from the next stage
        for i in range(len(rep_stages)):
            if i < len(rep_stages) - 1:
                stage = rep_stages[i]
                next_stage = rep_stages[i + 1]

                stage.score = next_stage.score
                stage.lives = next_stage.lives
                stage.th09_p2_score = next_stage.th09_p2_score
            else:
                stage = rep_stages[i]
                stage.score = None
                stage.lives = None
                stage.th09_p2_score = None

    else:
        #   vs mode
        p1 = replay.stages[9]
        p2 = replay.stages[19]

        r_shot = shots[p1.shot]
        r_score = p1.score * 10

        s = ReplayStage()
        s.stage = 1
        s.score = p1.score * 10
        s.th09_p1_cpu = p1.ai
        s.th09_p2_cpu = p2.ai
        s.th09_p2_shot = shots[p2.shot]
        s.th09_p2_score = p2.score * 10

        if s.th09_p1_cpu is False and s.th09_p2_cpu is False:
            r_type = game_ids.ReplayTypes.PVP  # mark pvp replays as such
        else:
            r_type = (
                game_ids.ReplayTypes.STAGE_PRACTICE
            )  # treat any "pvp" replay with an ai in it as stage practice

        rep_stages.append(s)

    r = ReplayInfo(
        game=game_ids.GameIDs.TH09,
        shot=r_shot,
        difficulty=replay.header.difficulty,
        score=r_score,
        timestamp=time.strptime(replay.header.date, "%y/%m/%d"),
        name=replay.header.name.replace("\x00", ""),
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse10(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0xAA, 0xE1)
    td.decrypt(comp_data, 0x80, 0x3D, 0x7A)
    replay = th10.Th10.from_bytes(td.unlzss(comp_data))

    shots = ["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"]

    rep_stages = []

    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage_num,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score * 10
            s.power = next_stage_start_data.power
            s.piv = next_stage_start_data.piv * 10
            s.lives = next_stage_start_data.lives
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH10,
        shot=shots[replay.header.shot * 3 + replay.header.subshot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse11(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x800, 0xAA, 0xE1)
    td.decrypt(comp_data, 0x40, 0x3D, 0x7A)
    replay = th11.Th11.from_bytes(td.unlzss(comp_data))

    shots = ["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"]

    rep_stages = []

    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage_num,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score * 10
            s.power = next_stage_start_data.power
            s.piv = next_stage_start_data.piv
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH11,
        shot=shots[replay.header.shot * 3 + replay.header.subshot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse12(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x800, 0x5E, 0xE1)
    td.decrypt(comp_data, 0x40, 0x7D, 0x3A)
    replay = th12.Th12.from_bytes(td.unlzss(comp_data))

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SanaeA", "SanaeB"]

    rep_stages = []

    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage_num,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score * 10
            s.power = next_stage_start_data.power
            s.piv = convert_stored_PIV_to_displayed(game_ids.GameIDs.TH12, next_stage_start_data.piv)
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            #   fix zun fuckery
            if s.life_pieces > 0:
                s.life_pieces -= 1
            s.bombs = next_stage_start_data.bombs
            s.bomb_pieces = next_stage_start_data.bomb_pieces
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH12,
        shot=shots[replay.header.shot * 2 + replay.header.subshot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse13(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0x5C, 0xE1)
    td.decrypt(comp_data, 0x100, 0x7D, 0x3A)
    replay = th13.Th13.from_bytes(td.unlzss(comp_data))

    shots = ["Reimu", "Marisa", "Sanae", "Youmu"]

    rep_stages = []

    if replay.header.spell_practice_id != 0xFFFFFFFF:
        return ReplayInfo(
            game=game_ids.GameIDs.TH13,
            shot=shots[replay.header.shot],
            difficulty=replay.header.difficulty,
            score=replay.header.score * 10,
            timestamp=datetime.datetime.fromtimestamp(
                replay.header.timestamp, tz=datetime.timezone.utc
            ),
            name=replay.header.name.replace("\x00", ""),
            slowdown=replay.header.slowdown,
            replay_type=game_ids.ReplayTypes.SPELL_PRACTICE,
            spell_card_id=replay.header.spell_practice_id,
        )

    # TH13 stores stage data values from the start of the stage but score from the end
    for current_stage, next_stage in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage.stage_num,
            score=replay.header.score * 10
        )
        if next_stage is not None:
            s.score = next_stage.score * 10
            s.power = next_stage.power
            # piv is stored with extra precision, we trunctate the value to what is shown ingame
            s.piv = convert_stored_PIV_to_displayed(game_ids.GameIDs.TH13, next_stage.piv)
            s.lives = next_stage.lives
            s.life_pieces = next_stage.life_pieces
            s.bombs = next_stage.bombs
            s.bomb_pieces = next_stage.bomb_pieces
            s.graze = next_stage.graze
            s.th13_trance = next_stage.trance
            s.extends = next_stage.extends
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH13,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse14(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0x5C, 0xE1)
    td.decrypt(comp_data, 0x100, 0x7D, 0x3A)
    replay = th14.Th14.from_bytes(td.unlzss(comp_data))

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"]
    rep_stages = []

    if replay.header.spell_practice_id != 0xFFFFFFFF:
        return ReplayInfo(
            game=game_ids.GameIDs.TH14,
            shot=shots[replay.header.shot * 2 + replay.header.subshot],
            difficulty=replay.header.difficulty,
            score=replay.header.score * 10,
            timestamp=datetime.datetime.fromtimestamp(
                replay.header.timestamp, tz=datetime.timezone.utc
            ),
            name=replay.header.name.replace("\x00", ""),
            slowdown=replay.header.slowdown,
            replay_type=game_ids.ReplayTypes.SPELL_PRACTICE,
            spell_card_id=replay.header.spell_practice_id,
        )

    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage_num,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score * 10
            s.power = next_stage_start_data.power
            s.piv = convert_stored_PIV_to_displayed(game_ids.GameIDs.TH14, next_stage_start_data.piv)
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            s.bombs = next_stage_start_data.bombs
            s.bomb_pieces = next_stage_start_data.bomb_pieces
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH14,
        shot=shots[replay.header.shot * 2 + replay.header.subshot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse15(rep_raw) -> ReplayInfo:
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0x5C, 0xE1)
    td.decrypt(comp_data, 0x100, 0x7D, 0x3A)
    replay = th15.Th15.from_bytes(td.unlzss(comp_data))

    shots = ["Reimu", "Marisa", "Sanae", "Reisen"]
    rep_stages = []
    
    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage_num,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score * 10
            s.power = next_stage_start_data.power
            s.piv = convert_stored_PIV_to_displayed(game_ids.GameIDs.TH15, next_stage_start_data.piv)
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            s.bombs = next_stage_start_data.bombs
            s.bomb_pieces = next_stage_start_data.bomb_pieces
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH15,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse16(rep_raw) -> ReplayInfo:
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0x5C, 0xE1)
    td.decrypt(comp_data, 0x100, 0x7D, 0x3A)
    replay = th16.Th16.from_bytes(td.unlzss(comp_data))

    def get_shot(shot_id: int, season_id: int) -> str:
        shots = ["Reimu", "Cirno", "Aya", "Marisa"]
        seasons = ["Spring", "Summer", "Autumn", "Winter", ""]
        return shots[shot_id] + seasons[season_id]

    if _is_spell_practice_modern(replay.header):
        return ReplayInfo(
            game=game_ids.GameIDs.TH16,
            shot=get_shot(replay.header.shot, replay.header.season),
            difficulty=replay.header.difficulty,
            score=replay.header.score * 10,
            timestamp=datetime.datetime.fromtimestamp(
                replay.header.timestamp, tz=datetime.timezone.utc
            ),
            name=replay.header.name.replace("\x00", ""),
            slowdown=replay.header.slowdown,
            replay_type=game_ids.ReplayTypes.SPELL_PRACTICE,
            spell_card_id=replay.header.spell_practice_id,
        )

    rep_stages = []
    
    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage_num,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score * 10
            s.power = next_stage_start_data.power
            s.piv = convert_stored_PIV_to_displayed(game_ids.GameIDs.TH16, next_stage_start_data.piv)
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            s.bombs = next_stage_start_data.bombs
            s.bomb_pieces = next_stage_start_data.bomb_pieces
            s.graze = next_stage_start_data.graze
            s.th16_season_power = next_stage_start_data.season_power
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH16,
        shot=get_shot(replay.header.shot, replay.header.season),
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse17(rep_raw) -> ReplayInfo:
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0x5C, 0xE1)
    td.decrypt(comp_data, 0x100, 0x7D, 0x3A)
    replay = th17.Th17.from_bytes(td.unlzss(comp_data))

    def get_shot(shot_id: int, subshot_id: int) -> str:
        shots = ["Reimu", "Marisa", "Youmu"]
        seasons = ["Wolf", "Otter", "Eagle"]
        return shots[shot_id] + seasons[subshot_id]

    if _is_spell_practice_modern(replay.header):
        return ReplayInfo(
            game=game_ids.GameIDs.TH17,
            shot=get_shot(replay.header.shot, replay.header.subshot),
            difficulty=replay.header.difficulty,
            score=replay.header.score * 10,
            timestamp=datetime.datetime.fromtimestamp(
                replay.header.timestamp, tz=datetime.timezone.utc
            ),
            name=replay.header.name.replace("\x00", ""),
            slowdown=replay.header.slowdown,
            replay_type=game_ids.ReplayTypes.SPELL_PRACTICE,
            spell_card_id=replay.header.spell_practice_id,
        )

    rep_stages = []
    
    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage_num,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score * 10
            s.power = next_stage_start_data.power
            s.piv = convert_stored_PIV_to_displayed(game_ids.GameIDs.TH17, next_stage_start_data.piv)
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            s.bombs = next_stage_start_data.bombs
            s.bomb_pieces = next_stage_start_data.bomb_pieces
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH17,
        shot=get_shot(replay.header.shot, replay.header.subshot),
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _Parse18(rep_raw) -> ReplayInfo:
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0x5C, 0xE1)
    td.decrypt(comp_data, 0x100, 0x7D, 0x3A)
    replay = th18.Th18.from_bytes(td.unlzss(comp_data))

    shots = ["Reimu", "Marisa", "Sakuya", "Sanae"]

    if _is_spell_practice_modern(replay.header):
        return ReplayInfo(
            game=game_ids.GameIDs.TH18,
            shot=shots[replay.header.shot],
            difficulty=replay.header.difficulty,
            score=replay.header.score * 10,
            timestamp=datetime.datetime.fromtimestamp(
                replay.header.timestamp, tz=datetime.timezone.utc
            ),
            name=replay.header.name.replace("\x00", ""),
            slowdown=replay.header.slowdown,
            replay_type=game_ids.ReplayTypes.SPELL_PRACTICE,
            spell_card_id=replay.header.spell_practice_id,
        )

    rep_stages = []

    for current_stage, next_stage in zip(replay.stages, replay.stages[1:] + [None]):
        current_stage_end_data = current_stage.stage_data_end
        s = ReplayStage(
            stage=current_stage.stage_num,
            power=current_stage_end_data.power,
            piv=convert_stored_PIV_to_displayed(game_ids.GameIDs.TH18, current_stage_end_data.piv),
            lives=current_stage_end_data.lives,
            life_pieces=current_stage_end_data.life_pieces,
            bombs=current_stage_end_data.bombs,
            bomb_pieces=current_stage_end_data.bomb_pieces,
            graze=current_stage_end_data.graze,
        )
        if next_stage is not None:
            # The end-of-stage data does not add the stage's clear bonus.
            # Therefore, we have to use the next stage's data.
            s.score = next_stage.stage_data_start.score * 10
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.REGULAR
    if len(rep_stages) == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH18,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
        stages=rep_stages,
    )

    return r


def _DetermineTH13orTH14(replay):
    # thank you ZUN
    # yes, one of the only indications of which game a replay is from here is from a USERDATA string
    header = th_modern.ThModern.from_bytes(replay)
    if header.userdata.user_desc[4] == "廟":
        # the raw byte is 0x90 or 144
        # you'll get that if you encode to 'shift_jis' and test the byte then
        return _Parse13(replay)
    elif header.userdata.user_desc[4] == "城":
        # the raw byte is 0x8b or 139
        return _Parse14(replay)
    # if its not either of the two above, then I don't know
    raise ValueError()


def _is_spell_practice_modern(replay_header) -> bool:
    return replay_header.spell_practice_id != 0xFFFFFFFF


def Parse(replay) -> ReplayInfo:
    """Parse a replay file."""

    # If replay is a memoryview, cast it to bytes.
    if isinstance(replay, memoryview):
        replay = bytes(replay)

    gamecode = replay[:4]

    try:
        if gamecode == b"T6RP":
            return _Parse06(replay)
        elif gamecode == b"T7RP":
            return _Parse07(replay)
        elif gamecode == b"T8RP":
            return _Parse08(replay)
        elif gamecode == b"T9RP":
            return _Parse09(replay)
        elif gamecode == b"t10r":
            return _Parse10(replay)
        elif gamecode == b"t11r":
            return _Parse11(replay)
        elif gamecode == b"t12r":
            return _Parse12(replay)
        elif gamecode == b"t13r":
            # ZUN was drunk and did not change the gamecode for TH14, so this is now used for two games
            # and thus we have to do fuckery to find which one it is
            # fun fact: the games themselves don't test this so if you rename the file you can crash them
            return _DetermineTH13orTH14(replay)
        elif gamecode == b"t15r":
            return _Parse15(replay)
        elif gamecode == b"t16r":
            return _Parse16(replay)
        elif gamecode == b"t17r":
            return _Parse17(replay)
        elif gamecode == b"t18r":
            return _Parse18(replay)
        else:
            logging.warning("Failed to comprehend gamecode %s", str(gamecode))
            raise UnsupportedGameError("This game is unsupported.")
    except (ValueError, IndexError, EOFError, KaitaiStructError):
        raise BadReplayError("This replay is corrupted or otherwise malformed")
