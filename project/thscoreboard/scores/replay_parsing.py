
from dataclasses import dataclass
import logging

class Error(Exception):
    pass


class BadReplayError(Error):
    pass

class UnsupportedGameError(Error):
    pass


class UnsupportedReplayError(Error):
    pass


def Parse(replay):
    """Parse a replay file."""

    gamecode = replay[:4]
    logging.info('gamecode %s', gamecode)

    if gamecode == b'T6RP':
        return _Parse06(replay)
    else:
        raise UnsupportedGameError('This game is unsupported.')

def _Parse06(replay):
    # Big thanks to https://pytouhou.linkmauve.fr/doc/06/t6rp.xhtml
    if len(replay) < 16:
        raise BadReplayError()

    header, rest = _Parse06Header(replay)
    decrypted_rest = _Decrypt06(header, rest)
    encrypted_header = _Parse06EncryptedHeader(decrypted_rest)

    logging.info(str(header))
    logging.info(str(encrypted_header))
    raise UnsupportedReplayError()

def _Parse06Header(replay):
    logging.info(replay[:15].hex())

    gamecode = replay[:4]
    version = replay[4:6]
    player_byte = replay[6]
    if player_byte == 0:
        player = 'ReimuA'
    elif player_byte == 1:
        player = 'ReimuB'
    elif player_byte == 2:
        player = 'MarisaA'
    elif player_byte == 3:
        player = 'MarisaB'
    else:
        raise BadReplayError('Could not read shot type')
    difficulty = replay[7]
    if difficulty > 4:
        raise BadReplayError('Could not recognize difficulty')
    checksum = replay[8:12]
    unused = replay[12:14]
    encryption_key = replay[14]
    rest = replay[15:]
    return (
        Touhou06Header(
            gamecode=gamecode,
            version=version,
            shot=player,
            difficulty=difficulty,
            checksum=checksum,
            encryption_key=encryption_key),
        rest)

def _Decrypt06(header, rest):
    def DecryptGenerator():
        key = header.encryption_key
        for byte in rest:
            yield (byte - key) % 256
            key += 7
    return bytes(DecryptGenerator())


def _ReadNullTerminatedAsciiString(some_bytes):
    for i, b in enumerate(some_bytes):
        if b == 0:
            return some_bytes[:i].decode(encoding='ascii')
    raise BadReplayError('Could not read bytestring')


def _Parse06EncryptedHeader(decrypted_rest):
    logging.info(decrypted_rest[:(37 + 6 * 4)].hex())
    # 1 ignored byte
    date_bytes = decrypted_rest[1:10]
    date_str = _ReadNullTerminatedAsciiString(date_bytes)
    name_bytes = decrypted_rest[10:19]
    name_str = _ReadNullTerminatedAsciiString(name_bytes)
    # 2 ignored bytes
    score = int.from_bytes(decrypted_rest[21:25], 'little', signed=False)
    # 4 ignored bytes
    # Some sources indicate that this is a floating point representation of
    # the slowdown rate. However, I can't get this to work.
    slowdown_rate_bytes = decrypted_rest[29:33]
    # 4 ignored bytes
    stage_n_offset = []
    for i in range(7):
        start_offset = 37 + i * 4
        stage_n_offset.append(int.from_bytes(decrypted_rest[start_offset:start_offset + 4], 'little', signed=False))

    return Touhou06EncryptedHeader(date_str, name_str, score, tuple(stage_n_offset))

@dataclass(frozen=True)
class Touhou06Header:
    gamecode: bytes  # 4 bytes
    version: bytes  # 4 bytes
    shot: str  # "ReimuA" etc
    difficulty: int  # 0 is easy, 1 normal, 4 extra
    checksum: bytes  # 4 bytes
    # Unused bit that is 2 bytes
    encryption_key: int  # 8-bit unsigned int

@dataclass(frozen=True)
class Touhou06EncryptedHeader:
    date: str
    name: str
    score: int
    stage_offsets: tuple  # Byte offsets where the per-stage entry starts.
    # Includes the unencrypted header's bytes!
