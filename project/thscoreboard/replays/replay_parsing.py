"""Parsing and gleaning information from individual replay files."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from kaitaistruct import KaitaiStructError

from . import game_ids
from .kaitai_parsers import th06
from .kaitai_parsers import th07
from .kaitai_parsers import th08
from .kaitai_parsers import th10
from .kaitai_parsers import th11
from .kaitai_parsers import th_modern

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


@dataclass
class ReplayStage:
    stage: int = None
    score: int = None
    piv: int = None
    graze: int = None
    point_items: int = None
    power: int = None
    lives: int = None
    life_pieces: int = None
    bombs: int = None
    bomb_pieces: int = None
    th06_rank: int = None
    th07_cherry: int = None
    th07_cherrymax: int = None

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class ReplayInfo:
    game: str
    shot: str
    difficulty: int
    score: int
    timestamp: datetime
    name: str
    route: Optional[str] = None
    stages = []


def _Parse06(rep_raw):
    cryptdata = bytearray(rep_raw[15:])
    td.decrypt06(cryptdata, rep_raw[14])
    replay = th06.Th06.from_bytes(cryptdata)

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]

    rep_stages = []
    i = 0
    for score in replay.stages:
        if replay.header.stage_offsets[i] != 0:
            s = ReplayStage()
            s.stage = i
            s.score = score.score
            s.power = score.power
            s.lives = score.lives
            s.bombs = score.bombs
            s.th06_rank = score.rank
            rep_stages.append(s)
        i += 1

    r = ReplayInfo(
        game=game_ids.GameIDs.TH06,
        shot=shots[rep_raw[6]],
        difficulty=rep_raw[7],
        score=replay.header.score,
        timestamp=datetime.strptime(replay.header.date, "%m/%d/%y"),
        name=replay.header.name.replace("\x00", "")
    )

    r.stages = rep_stages

    return r


def _Parse07(rep_raw):
    comp_data = bytearray(rep_raw[16:])
    td.decrypt06(comp_data, rep_raw[13])
    #   please don't ask what is going on here
    #   0x54 - 16 = 68
    replay = th07.Th07.from_bytes(bytearray(16) + comp_data[0:68] + td.unlzss(comp_data[68:]))

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"]

    rep_stages = []

    i = 0
    for score in replay.stages:
        if replay.file_header.stage_offsets[i] != 0:
            s = ReplayStage()
            s.stage = i
            s.score = score.score * 10
            s.power = score.power
            s.lives = score.lives
            s.bombs = score.bombs
            s.point_items = score.point_items
            s.graze = score.graze
            s.piv = score.piv
            s.th07_cherry = score.cherry
            s.th07_cherrymax = score.cherrymax
            rep_stages.append(s)
        i += 1

    r = ReplayInfo(
        game=game_ids.GameIDs.TH07,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.strptime(replay.header.date, "%m/%d"),
        name=replay.header.name.replace("\x00", "")
    )

    r.stages = rep_stages
    return r


def _Parse08(rep_raw):
    comp_data = bytearray(rep_raw[24:])
    td.decrypt06(comp_data, rep_raw[21])
    #   basically copied from _Parse07()
    #   0x68 (104) - 24 = 80
    replay = th08.Th08.from_bytes(bytearray(24) + comp_data[0:80] + td.unlzss(comp_data[80:]))
    
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
        "Yuyuko"
    ]

    rep_stages = []

    i = 0
    route = None
    for score in replay.stages:
        if replay.file_header.stage_offsets[i] != 0:
            s = ReplayStage()
            s.stage = i
            s.score = score.score * 10
            s.power = score.power
            s.lives = score.lives
            s.bombs = score.bombs
            s.point_items = score.point_items
            s.graze = score.graze
            s.piv = score.piv
            if i == 6:
                route = 'Final A'
            elif i == 7:
                route = 'Final B'
            rep_stages.append(s)
        i += 1

    r = ReplayInfo(
        game=game_ids.GameIDs.TH08,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.strptime(replay.header.date, "%m/%d"),
        name=replay.header.name.replace("\x00", ""),
        route=route
    )

    r.stages = rep_stages
    return r


def _Parse10(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0xaa, 0xe1)
    td.decrypt(comp_data, 0x80, 0x3d, 0x7a)
    replay = th10.Th10.from_bytes(td.unlzss(comp_data))

    shots = ["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"]

    rep_stages = []
    for stage in replay.stages:
        s = ReplayStage()
        s.stage = stage.stage
        s.score = stage.score * 10
        s.power = stage.power
        s.piv = stage.piv
        s.lives = stage.lives
        rep_stages.append(s)

    r = ReplayInfo(
        game=game_ids.GameIDs.TH10,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.fromtimestamp(replay.header.timestamp),
        name=replay.header.name.replace("\x00", "")
    )

    r.stages = rep_stages

    return r


def _Parse11(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x800, 0xaa, 0xe1)
    td.decrypt(comp_data, 0x40, 0x3d, 0x7a)
    replay = th11.Th11.from_bytes(td.unlzss(comp_data))

    shots = ["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"]

    rep_stages = []
    for stage in replay.stages:
        s = ReplayStage()
        s.stage = stage.stage
        s.score = stage.score * 10
        s.piv = stage.piv
        s.graze = stage.graze
        s.power = stage.power
        s.lives = stage.lives
        s.life_pieces = stage.life_pieces
        rep_stages.append(s)

    r = ReplayInfo(
        game=game_ids.GameIDs.TH11,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.fromtimestamp(replay.header.timestamp),
        name=replay.header.name.replace("\x00", "")
    )

    r.stages = rep_stages

    return r


def Parse(replay):
    """Parse a replay file."""

    gamecode = replay[:4]

    try:
        if gamecode == b'T6RP':
            return _Parse06(replay)
        elif gamecode == b'T7RP':
            return _Parse07(replay)
        elif gamecode == b'T8RP':
            return _Parse08(replay)
        elif gamecode == b't10r':
            return _Parse10(replay)
        elif gamecode == b't11r':
            return _Parse11(replay)
        else:
            logging.warning('Failed to comprehend gamecode %s', gamecode)
            raise UnsupportedGameError('This game is unsupported.')
    except (ValueError, IndexError, EOFError, KaitaiStructError):
        raise BadReplayError('This replay is corrupted or otherwise malformed')
