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

def Parse(replay):
    """Parse a replay file."""

    gamecode = replay[:4]
    logging.info('gamecode %s', gamecode)

    if gamecode == b'T6RP':
        from .replay_parsers import th06
        get_real = th06.Th06.from_bytes(bytes(th06_decrypt(replay[15:], replay[14])))
        
        shots = [ "ReimuA", "ReimuB", "MarisaA", "MarisaB" ]        
        
        return ReplayInfo(
            game_ids.GameIDs.TH06,
            shots[replay[6]],
            replay[7],
            get_real.header.score
        )
    else:
        raise UnsupportedGameError('This game is unsupported.')
