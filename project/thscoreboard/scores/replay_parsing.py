"""Parsing and gleaning information from individual replay files."""

from dataclasses import dataclass
import logging

from . import game_ids
from .kaitai_parsers import th06
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


# LZSS decompression code written by Michael Lamparski (ExpHP)
# From his Samidare archive extractor and repacker (samidare.py)

def _iter_take(iter, n):
    """ Limit an iterator to just the first n elements. """
    for _ in range(n):
        try:
            yield next(iter)
        except StopIteration:
            return


def _read_integer_from_bitstream(bit_iter, size):
    """ Read ``size`` bytes from bit_iter as an integer in big-endian bit order.

    Bits after the end of the iterator can be read, and will be zero."""
    int_bits = list(_iter_take(bit_iter, size))
    int_bits.extend([0] * (size - len(int_bits)))

    acc = 0
    for bit in int_bits:
        acc *= 2
        acc += bit
    return acc


def _expect_iter_empty(iter):
    try:
        value = next(iter)
    except StopIteration:
        return
    assert False, f'iterator not empty (item: {value})'


def _unlzss(input_bytes):
    # Iterate over the bits as a bit stream, from MSB to LSB for each byte
    concatenated_bits = ''.join([f'{x:08b}' for x in input_bytes])
    input_bits = iter([int(bitstr) for bitstr in concatenated_bits])

    # Keep scrolling window of previous output
    history = [0] * 0x8000
    history_write_index = 1
    output_bytes = []
    
    def put_output_byte(byte: int):
        nonlocal history_write_index
        output_bytes.append(byte)
        history[history_write_index] = byte
        history_write_index += 1
        history_write_index %= len(history)

    while True:
        control_bit = _read_integer_from_bitstream(input_bits, 1)
        if control_bit:
            # Directly read an output byte
            data_byte = _read_integer_from_bitstream(input_bits, 8)
            put_output_byte(data_byte)
            # print('<-- new data byte ({:04x}):  {}', history_write_index, repr(bytes([data_byte])))

        else:
            # Read a string from the history
            read_from = _read_integer_from_bitstream(input_bits, 15)
            if not read_from:
                # print(' no more bits:  exit')
                break
            # print(f'--> read from: {read_from}')
            read_count = _read_integer_from_bitstream(input_bits, 4) + 3

            # Read a string from the history.
            #
            # IMPORTANT:
            #    Each new byte must be added to the history immediately after it is read.
            #    This is because it is possible for the range `read_from:read_from + read_count`
            #    to cross over the current write point in the history.
            #    (allowing a byte or a short byte sequence to be repeated)
            for _ in range(read_count):
                put_output_byte(history[read_from])
                # print(f'      history: -> {repr(bytes([history[read_from]]))}')
                read_from += 1
                read_from %= len(history)

    _expect_iter_empty(input_bits)
    return bytes(output_bytes)


def _Parse06(rep_raw):
    replay = th06.Th06.from_bytes(bytes(_th06_decrypt(rep_raw[15:], rep_raw[14])))
    
    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]
    
    return ReplayInfo(
        game_ids.GameIDs.TH06,
        shots[rep_raw[6]],
        rep_raw[7],
        replay.header.score
    )


def _Parse10(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)
    
    _decrypt(comp_data, 0x400, 0xaa, 0xe1)
    _decrypt(comp_data, 0x80, 0x3d, 0x7a)

    replay = th10.Th10.from_bytes(_unlzss(comp_data))
    
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
    elif gamecode == b't10r':
        return _Parse10(replay)
    else:
        raise UnsupportedGameError('This game is unsupported.')
