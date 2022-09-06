"""Parsing and gleaning information from individual replay files."""

from dataclasses import dataclass
from datetime import datetime
import logging

from . import game_ids
from .kaitai_parsers import th06
from .kaitai_parsers import th07
from .kaitai_parsers import th10
from .kaitai_parsers import th_modern

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
class ReplayInfo:
    game: str
    shot: str
    difficulty: int
    score: int
    timestamp: datetime

    # def GetShotId(self):
    #     """Get the integer shot ID suitable for the database."""
    #     # This is kind of imprecise; fix up data structures so we don't need to do this.
    #     if self.game == game_ids.GameIDs.TH06:
    #         return game_ids.TH06_SHOT_NAME_TO_ID_BIDICT[self.shot]


def _Parse06(rep_raw):
    cryptdata = bytearray(rep_raw[15:])
    td.decrypt06(cryptdata, rep_raw[14])
    replay = th06.Th06.from_bytes(cryptdata)
    
    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]
    
    return ReplayInfo(
        game_ids.GameIDs.TH06,
        shots[rep_raw[6]],
        rep_raw[7],
        replay.header.score,
        datetime.strptime(replay.header.date, "%m/%d/%y")
    )


def _Parse07(rep_raw):
    comp_data = bytearray(rep_raw[16:])
    td.decrypt06(comp_data, rep_raw[13])
    #   please don't ask what is going on here
    #   0x54 - 16 = 68
    replay = th07.Th07.from_bytes(bytearray(16) + comp_data[0:68] + td.unlzss(comp_data[68:]))

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"]
    return ReplayInfo(
        game_ids.GameIDs.TH07,
        shots[replay.header.shot],
        replay.header.difficulty,
        replay.header.score * 10,
        datetime.strptime(replay.header.date, "%m/%d")
    )


def _Parse10(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)
    
    td.decrypt(comp_data, 0x400, 0xaa, 0xe1)
    td.decrypt(comp_data, 0x80, 0x3d, 0x7a)
    replay = th10.Th10.from_bytes(td.unlzss(comp_data))
    
    shots = ["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"]
      
    return ReplayInfo(
        game_ids.GameIDs.TH10,
        shots[replay.header.shot],
        replay.header.difficulty,
        replay.header.score * 10,
        datetime.fromtimestamp(replay.header.timestamp)
    )


def Parse(replay):
    """Parse a replay file."""

    gamecode = replay[:4]
    logging.info('gamecode %s', gamecode)

    if gamecode == b'T6RP':
        return _Parse06(replay)
    elif gamecode == b'T7RP':
        return _Parse07(replay)
    elif gamecode == b't10r':
        return _Parse10(replay)
    else:
        raise UnsupportedGameError('This game is unsupported.')
