"""Parsing and gleaning information from individual replay files."""

from dataclasses import dataclass
import logging

from . import game_ids

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

def th06_decrypt(data, key):
    for byte in data:
        yield (byte - key) % 256
        key += 7
    return data

def th_decrypt(data, block_size, base, add):
    assert isinstance(data, bytearray)
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

class Ref:
    def __init__(self, value):
        self.value = value

def get_bit(buffer, ref_pointer, ref_filter, length):
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
    
def th_unlzss(buffer, decode, length):
    ref_pointer = Ref(0)
    ref_filter = Ref(0x80)
    dest = 0
    dic = [0] * 0x2010
    while ref_pointer.value < length:
        bits = get_bit(buffer, ref_pointer, ref_filter, 1)
        if ref_pointer.value >= length:
            return dest
        if bits:
            bits = get_bit(buffer, ref_pointer, ref_filter, 8)
            if ref_pointer.value >= length:
                return dest
            decode[dest] = bits
            dic[dest & 0x1fff] = bits
            dest += 1
        else:
            bits = get_bit(buffer, ref_pointer, ref_filter, 13)
            if ref_pointer.value >= length:
                return dest
            index = bits - 1
            bits = get_bit(buffer, ref_pointer, ref_filter, 4)
            if ref_pointer.value >= length:
                return dest
            bits += 3
            for i in range(bits):
                dic[dest & 0x1fff] = dic[index + i]
                decode[dest] = dic[index + i]
                dest += 1
    return dest

def Parse(replay):
    """Parse a replay file."""

    gamecode = replay[:4]
    logging.info('gamecode %s', gamecode)

    if gamecode == b'T6RP':
        from .kaitai_parsers import th06
        get_real = th06.Th06.from_bytes(bytes(th06_decrypt(replay[15:], replay[14])))
        
        shots = [ "ReimuA", "ReimuB", "MarisaA", "MarisaB" ]        
        
        return ReplayInfo(
            game_ids.GameIDs.TH06,
            shots[replay[6]],
            replay[7],
            get_real.header.score
        )
    elif gamecode == b't10r':
        from .kaitai_parsers import th10
        from .kaitai_parsers import th_modern
        
        header = th_modern.ThModern.from_bytes(replay)
        comp_data = bytearray(header.main.comp_data)
        
        th_decrypt(comp_data, 0x400, 0xaa, 0xe1)
        th_decrypt(comp_data, 0x80, 0x3d, 0x7a)
        decodedata = bytearray(header.main.size)
        th_unlzss(comp_data, decodedata, header.main.comp_size-2)
        
        get_real = th10.Th10.from_bytes(decodedata)
        
        shots = [ "ReimuA", "ReimuB", "ReimuC", "MarisaA", "MarisaB", "MarisaC" ]

        logging.info("shot: %s\ndifficulty: %s\nscore: %s", get_real.header.shot, get_real.header.difficulty, get_real.header.score)

        return ReplayInfo(
            game_ids.GameIDs.TH10,
            shots[get_real.header.shot],
            get_real.header.difficulty,
            get_real.header.score * 10
        )

    else:
        raise UnsupportedGameError('This game is unsupported.')
