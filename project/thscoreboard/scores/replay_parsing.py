"""Parsing and gleaning information from individual replay files."""

from dataclasses import dataclass
import logging

from . import game_ids
from .kaitai_parsers import th06
from .kaitai_parsers import th07, th07_comp
from .kaitai_parsers import th10
from .kaitai_parsers import th_modern


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

    # def GetShotId(self):
    #     """Get the integer shot ID suitable for the database."""
    #     # This is kind of imprecise; fix up data structures so we don't need to do this.
    #     if self.game == game_ids.GameIDs.TH06:
    #         return game_ids.TH06_SHOT_NAME_TO_ID_BIDICT[self.shot]


def _th06_decrypt(data, key):
    for byte in data:
        yield (byte - key) % 256
        key += 7
    return data


def _decrypt(data: bytearray, block_size, base, add):
    tbuf = data.copy()
    p = 0
    left = len(data)
    if left % block_size < block_size // 4:
        left -= left % block_size
    left -= len(data) & 1
    while left:
        if left < block_size:
            block_size = left
        tp1 = p + block_size - 1
        tp2 = p + block_size - 2
        hf = (block_size + (block_size & 0x1)) // 2
        for i in range(hf):
            data[tp1] = tbuf[p] ^ base
            base = (base + add) % 0x100
            tp1 -= 2
            p += 1
        hf = block_size // 2
        for i in range(hf):
            data[tp2] = tbuf[p] ^ base
            base = (base + add) % 0x100
            tp2 -= 2
            p += 1
        left -= block_size


class _Ref:
    def __init__(self, value):
        self.value = value


def _unlzss_get_bit(buffer, ref_pointer, ref_filter, length):
    result = 0
    current = buffer[ref_pointer.value]
    for i in range(length):
        result <<= 1
        if current & ref_filter.value:
            result |= 0x1
        ref_filter.value >>= 1
        if ref_filter.value == 0:
            ref_pointer.value += 1
            current = buffer[ref_pointer.value]
            ref_filter.value = 0x80
    return result


def _unlzss(buffer, decode, length):
    ref_pointer = _Ref(0)
    ref_filter = _Ref(0x80)
    dest = 0
    dic = [0] * 0x2010
    while ref_pointer.value < length:
        bits = _unlzss_get_bit(buffer, ref_pointer, ref_filter, 1)
        if ref_pointer.value >= length:
            return dest
        if bits:
            bits = _unlzss_get_bit(buffer, ref_pointer, ref_filter, 8)
            if ref_pointer.value >= length:
                return dest
            decode[dest] = bits
            dic[dest & 0x1fff] = bits
            dest += 1
        else:
            bits = _unlzss_get_bit(buffer, ref_pointer, ref_filter, 13)
            if ref_pointer.value >= length:
                return dest
            index = bits - 1
            bits = _unlzss_get_bit(buffer, ref_pointer, ref_filter, 4)
            if ref_pointer.value >= length:
                return dest
            bits += 3
            for i in range(bits):
                dic[dest & 0x1fff] = dic[index + i]
                decode[dest] = dic[index + i]
                dest += 1
    return dest


def _Parse06(rep_raw):
    replay = th06.Th06.from_bytes(bytes(_th06_decrypt(rep_raw[15:], rep_raw[14])))
    
    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]
    
    return ReplayInfo(
        game_ids.GameIDs.TH06,
        shots[rep_raw[6]],
        rep_raw[7],
        replay.header.score
    )


def _Parse07(rep_raw):
    rep_raw = bytes(_th06_decrypt(rep_raw[16:], rep_raw[13]))
    header = th07_comp.Th07Comp.from_bytes(rep_raw)
    comp_data = bytearray(header.header.size)
    #   please don't ask what is going on here
    #   0x54 - 16 = 68
    _unlzss(rep_raw[68:], comp_data, header.header.comp_size - 2)
    comp_data = bytearray(16) + rep_raw[0:68] + comp_data
    replay = th07.Th07.from_bytes(comp_data)

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"]
    return ReplayInfo(
        game_ids.GameIDs.TH07,
        shots[replay.header.shot],
        replay.header.difficulty,
        replay.header.score * 10
    )


def _Parse10(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)
    
    _decrypt(comp_data, 0x400, 0xaa, 0xe1)
    _decrypt(comp_data, 0x80, 0x3d, 0x7a)
    decodedata = bytearray(header.main.size)
    _unlzss(comp_data, decodedata, header.main.comp_size - 2)
    
    replay = th10.Th10.from_bytes(decodedata)
    
    shots = ["ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC"]
      
    return ReplayInfo(
        game_ids.GameIDs.TH10,
        shots[replay.header.shot],
        replay.header.difficulty,
        replay.header.score * 10
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
