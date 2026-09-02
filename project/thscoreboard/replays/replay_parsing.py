import dataclasses
from typing import List, Optional
import datetime
import uuid
from kaitaistruct import KaitaiStructError

from replays.lib import time
from . import game_ids
from .kaitai_parsers import th03_v14
from .kaitai_parsers import th06
from .kaitai_parsers import th07
from .kaitai_parsers import th08
from .kaitai_parsers import th09
from .kaitai_parsers import th095_encrypted
from .kaitai_parsers import th10
from .kaitai_parsers import th11
from .kaitai_parsers import th12
from .kaitai_parsers import th128
from .kaitai_parsers import th13
from .kaitai_parsers import th14
from .kaitai_parsers import th15
from .kaitai_parsers import th16
from .kaitai_parsers import th17
from .kaitai_parsers import th18
from .kaitai_parsers import th20
from .kaitai_parsers import alco
from .kaitai_parsers import th_modern
from .kaitai_parsers import th_modern_20_header
from .kaitai_parsers import th08_userdata
from .kaitai_parsers import alco_userdata

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
    th128_motivation: int = None
    th128_perfect_freeze: int = None
    th128_frozen_area: float = None
    th13_trance: int = None
    extends: int = None
    th16_season_power: int = None
    th03_player_cpu: bool = None
    th03_opponent_cpu: bool = None
    th03_opponent_shot: str = None
    th03_opponent_score: int = None

    def __getitem__(self, item):
        return getattr(self, item)


@dataclasses.dataclass
class ReplayInfo:
    game: str
    shot: str
    score: int
    timestamp: Optional[datetime.datetime]
    """The timestamp for the replay.

    This field is either an aware datetime or None when the replay has no date.
    """

    name: str
    replay_type: int

    difficulty: Optional[int] = None
    route: Optional[str] = None

    spell_card_id: Optional[int] = None
    scene_game_level: Optional[int] = None
    scene_game_scene: Optional[int] = None

    stages: List[ReplayStage] = dataclasses.field(default_factory=list)
    slowdown: Optional[float] = None

    # Equipment chosen at the beginning of the game.
    # This is currently only used in th20, in which it is the stones selected
    # by the player.
    # The order is significant; in th20, the first incident stone is the "main"
    # stone.
    equipment: tuple[str] = dataclasses.field(default_factory=tuple)
    miss_count: Optional[int] = None
    is_clear: Optional[bool] = None
    th03_ruleset: Optional[int] = None
    th03_is_netplay: Optional[bool] = None
    th03_recorder_role: Optional[int] = None
    th03_recorder_source: Optional[int] = None
    th03_p1_uuid: Optional[str] = None
    th03_p2_uuid: Optional[str] = None
    th03_match_id: Optional[str] = None
    th03_p1_name: Optional[str] = None
    th03_p2_name: Optional[str] = None

    @property
    def spell_card_id_format(self):
        """Get frontend formatted spellcard id (1-indexed instead of 0-indexed)"""
        return self.spell_card_id + 1

    def __post_init__(self):
        if self.timestamp is not None and self.timestamp.tzinfo is None:
            # Why require the datetime be aware?
            # Basically, it's because Python timezone handling is a disaster.
            # datetimes without explicit timezone info tend to be converted
            # in weird ways by builtin methods, so it's way too easy to
            # accidentally apply a timezone correction twice.
            raise ValueError("timestamp datetime must be aware")


_TH03_SHOTS = [
    "Reimu",
    "Mima",
    "Marisa",
    "Ellen",
    "Kotohime",
    "Kana",
    "Rikako",
    "Chiyuri",
    "Yumemi",
]

_TH03_HEADER_SIZE = 896
_TH03_CHECKPOINT_SIZE = 289
_TH03_SUMMARY_FLAGS = 0x7F
_TH03_SCORE_UNKNOWN = 0xFF
_TH03_GAME_MODE_STORY = 1
_TH03_GAME_MODE_VS_1P_CPU = 0x80
_TH03_GAME_MODE_VS_1P_2P = 0x81
_TH03_GAME_MODE_VS_CPU_CPU = 0x82
_TH03_FLAG_RLE_INPUT = 0x0001
_TH03_FLAG_CHARGE_INPUT = 0x0002
_TH03_FLAG_PRACTICE = 0x0004
_TH03_FLAGS_KNOWN = _TH03_FLAG_RLE_INPUT | _TH03_FLAG_CHARGE_INPUT | _TH03_FLAG_PRACTICE
_TH03_RECORDING_FLAG_NETPLAY = 0x01
_TH03_END_REASON_COMPLETE = 1
_TH03_SUMMARY_UNKNOWN = 0xFF
_TH03_NAME_BYTES = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?")
_TH03_OLD_FORMAT_MESSAGE = (
    "This PoDD replay uses an older format. Please use the Replay Patch installer "
    "or Data Manager to update it to V14 before uploading."
)


def _TH03UnpackScore(score) -> int:
    value = 0
    multiplier = 1
    for packed_digits in score.digits:
        for digit in (packed_digits & 0x0F, packed_digits >> 4):
            if digit > 9:
                raise ValueError("Invalid packed score")
            value += digit * multiplier
            multiplier *= 10

    # PoDD internally stores the eight digits to the left of the always-zero
    # units digit.
    return value * 10


def _TH03UnpackPlaychar(playchar_paletted: int) -> str:
    # PlaycharPalettedOptional reserves 0 for no character, then stores the
    # alternate-palette bit below the character ID.
    if playchar_paletted < 1 or playchar_paletted > (len(_TH03_SHOTS) * 2):
        raise ValueError("Invalid PoDD character")
    return _TH03_SHOTS[(playchar_paletted - 1) // 2]


def _TH03ParseDosDate(dos_date: int) -> Optional[datetime.datetime]:
    if dos_date == 0:
        return None

    year = 1980 + (dos_date >> 9)
    month = (dos_date >> 5) & 0x0F
    day = dos_date & 0x1F
    return datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc)


def _TH03Uuid(value: bytes) -> Optional[str]:
    if not any(value):
        return None
    return str(uuid.UUID(bytes=value))


def _TH03FallbackNametag(raw: bytes, length: int) -> Optional[str]:
    if length > 57 or any(raw[length:]):
        raise ValueError("Invalid PoDD fallback nametag storage")
    value = raw[:length]
    if not value:
        return None
    if (
        value.startswith(b" ")
        or value.endswith(b" ")
        or b"  " in value
        or any(byte < 0x20 or byte > 0x7E for byte in value)
    ):
        raise ValueError("Invalid PoDD fallback nametag")

    lines = 1
    line_size = 0
    for word in value.split(b" "):
        if len(word) > 28:
            raise ValueError("PoDD fallback nametag does not fit")
        required = len(word) if line_size == 0 else line_size + 1 + len(word)
        if required > 28:
            lines += 1
            line_size = len(word)
            if lines > 2:
                raise ValueError("PoDD fallback nametag does not fit")
        else:
            line_size = required
    return value.decode("ascii")


def _TH03RoundSplits(replay):
    if replay.summary.round_reached_count > len(replay.summary.round_splits):
        raise ValueError("Invalid PoDD round split count")
    return replay.summary.round_splits[: replay.summary.round_reached_count]


def _TH03LatestRoundSplit(round_splits, stage: int):
    matching_splits = [
        split for split in round_splits if (split.stage_round & 0x0F) == stage
    ]
    if not matching_splits:
        return None
    return max(matching_splits, key=lambda split: split.stage_round >> 4)


def _TH03StoryStageLives(replay) -> list[Optional[int]]:
    """Return exact end-of-stage stock from the next stage checkpoint.

    The first checkpoint for the following stage contains the stock left after
    the previous stage, including score extends and losses. The header contains
    the same authoritative value for the final reached stage, including an
    unfinished stage ended through the pause menu.
    """

    first_checkpoint_by_stage = {}
    for index in range(replay.summary.checkpoint_count):
        stage_round = replay.summary.checkpoint_stage_round[index]
        stage = stage_round & 0x0F
        checkpoint = replay.checkpoints[index]
        first_checkpoint_by_stage.setdefault(stage, checkpoint)

    stage_lives = []
    for stage in range(replay.stage_reached_count):
        if stage == (replay.stage_reached_count - 1):
            lives = replay.final_story_lives
        else:
            next_stage = first_checkpoint_by_stage.get(stage + 1)
            lives = next_stage.snapshot.story_lives if next_stage else None

        if lives == _TH03_SUMMARY_UNKNOWN:
            lives = None
        stage_lives.append(lives)

    return stage_lives


def _TH03Validate(replay) -> None:
    if (replay.flags & (_TH03_FLAG_RLE_INPUT | _TH03_FLAG_CHARGE_INPUT)) != (
        _TH03_FLAG_RLE_INPUT | _TH03_FLAG_CHARGE_INPUT
    ) or replay.flags & ~_TH03_FLAGS_KNOWN:
        raise ValueError("Unsupported PoDD input encoding")
    if replay.status != 2:
        raise ValueError("PoDD replay was not finalized")
    if replay.end_reason > 6:
        raise ValueError("Invalid PoDD replay end reason")
    if replay.game_mode not in (
        _TH03_GAME_MODE_STORY,
        _TH03_GAME_MODE_VS_1P_CPU,
        _TH03_GAME_MODE_VS_1P_2P,
        _TH03_GAME_MODE_VS_CPU_CPU,
    ):
        raise ValueError("Unsupported PoDD game mode")

    if replay.flags & _TH03_FLAG_PRACTICE:
        raise UnsupportedReplayError("PoDD Practice replays are not supported.")
    if replay.game_mode == _TH03_GAME_MODE_VS_CPU_CPU:
        raise UnsupportedReplayError("PoDD CPU vs CPU replays are not supported.")
    if replay.rank > 3 or replay.key_mode > 2:
        raise ValueError("Invalid PoDD game settings")
    if replay.is_cpu_p1 > 1 or replay.is_cpu_p2 > 1 or replay.autofire > 3:
        raise ValueError("Invalid PoDD player settings")
    expected_cpu = (0, 0) if replay.game_mode == _TH03_GAME_MODE_VS_1P_2P else (0, 1)
    if (replay.is_cpu_p1, replay.is_cpu_p2) != expected_cpu:
        raise ValueError("PoDD CPU flags disagree with the game mode")
    if replay.sample_count == 0 or replay.input_size == 0:
        raise ValueError("Empty PoDD replay")
    if replay.stage_reached_count > 9 or (
        replay.game_mode != _TH03_GAME_MODE_STORY and replay.stage_reached_count != 0
    ):
        raise ValueError("Invalid PoDD stage count")
    if replay.game_mode == _TH03_GAME_MODE_STORY and replay.story_stage >= 9:
        raise ValueError("Invalid PoDD initial Story stage")

    netplay = bool(replay.recording_flags & _TH03_RECORDING_FLAG_NETPLAY)
    if replay.ruleset != 0 or replay.recording_flags & ~_TH03_RECORDING_FLAG_NETPLAY:
        raise ValueError("Invalid PoDD V14 rules metadata")
    if replay.recorder_role > 2 or replay.recorder_source > 3:
        raise ValueError("Invalid PoDD V14 recorder metadata")
    if netplay != bool(replay.recorder_role):
        raise ValueError("Inconsistent PoDD V14 netplay ownership")
    if netplay and replay.game_mode != _TH03_GAME_MODE_VS_1P_2P:
        raise ValueError("Invalid PoDD V14 netplay game mode")
    _TH03FallbackNametag(replay.player_one_nametag, replay.player_one_nametag_length)
    _TH03FallbackNametag(replay.player_two_nametag, replay.player_two_nametag_length)
    if replay.summary_flags != _TH03_SUMMARY_FLAGS:
        raise ValueError("Outdated PoDD replay summary")
    if replay.summary.flags != _TH03_SUMMARY_FLAGS:
        raise ValueError("Outdated PoDD round summary")
    if replay.summary.slow_frames > replay.summary.timed_frames:
        raise ValueError("Invalid PoDD slowdown counters")
    if replay.final_route != _TH03_SUMMARY_UNKNOWN and replay.final_route > 2:
        raise ValueError("Invalid PoDD final route")
    if (
        replay.final_game_mode != _TH03_SUMMARY_UNKNOWN
        and replay.final_game_mode
        not in (
            _TH03_GAME_MODE_STORY,
            _TH03_GAME_MODE_VS_1P_CPU,
            _TH03_GAME_MODE_VS_1P_2P,
            _TH03_GAME_MODE_VS_CPU_CPU,
        )
    ):
        raise ValueError("Invalid PoDD final game mode")
    if (
        replay.final_story_stage != _TH03_SUMMARY_UNKNOWN
        and replay.final_story_stage > 9
    ):
        raise ValueError("Invalid PoDD final Story stage")
    if replay.final_winner != _TH03_SUMMARY_UNKNOWN and replay.final_winner > 1:
        raise ValueError("Invalid PoDD final winner")
    if replay.game_mode == _TH03_GAME_MODE_STORY:
        checkpoint_capacity = 15
    else:
        checkpoint_capacity = 3

    expected_input_offset = _TH03_HEADER_SIZE + (
        checkpoint_capacity * _TH03_CHECKPOINT_SIZE
    )
    if replay.input_offset != expected_input_offset:
        raise ValueError("Invalid PoDD input offset")
    if len(replay.checkpoints) != checkpoint_capacity:
        raise ValueError("Invalid PoDD checkpoint reservation")
    if not 1 <= replay.summary.checkpoint_count <= checkpoint_capacity:
        raise ValueError("Invalid PoDD checkpoint count")
    if replay.checkpoints[0].snapshot.autofire != replay.autofire:
        raise ValueError("Inconsistent PoDD autofire setting")

    _TH03UnpackPlaychar(replay.playchar_p1)
    _TH03UnpackPlaychar(replay.playchar_p2)
    _TH03UnpackScore(replay.final_score)
    if any(replay.name) and any(byte not in _TH03_NAME_BYTES for byte in replay.name):
        raise ValueError("Invalid PoDD replay name")


def _Parse03(rep_raw):
    if rep_raw[:8] in (b"T3RPLY11", b"T3RPLY12", b"T3RPLY13"):
        raise UnsupportedReplayError(_TH03_OLD_FORMAT_MESSAGE)
    if rep_raw[:8] != b"T3RPLY14":
        raise ValueError("Unsupported PoDD replay version")
    replay = th03_v14.Th03V14.from_bytes(rep_raw)
    _TH03Validate(replay)

    round_splits = _TH03RoundSplits(replay)
    p1_shot = _TH03UnpackPlaychar(replay.playchar_p1)
    p2_shot = _TH03UnpackPlaychar(replay.playchar_p2)
    final_score = _TH03UnpackScore(replay.final_score)
    netplay = bool(replay.recording_flags & _TH03_RECORDING_FLAG_NETPLAY)
    stages = []

    if replay.game_mode == _TH03_GAME_MODE_STORY:
        replay_type = game_ids.ReplayTypes.FULL_GAME
        stage_lives = _TH03StoryStageLives(replay)
        for stage_index in range(replay.stage_reached_count):
            opponent = _TH03UnpackPlaychar(replay.story.stage_opponents[stage_index])
            round_split = _TH03LatestRoundSplit(round_splits, stage_index)
            stages.append(
                ReplayStage(
                    stage=stage_index + 1,
                    score=_TH03UnpackScore(replay.story.stage_scores[stage_index]),
                    lives=stage_lives[stage_index],
                    th03_player_cpu=bool(replay.is_cpu_p1),
                    th03_opponent_cpu=bool(replay.is_cpu_p2),
                    th03_opponent_shot=opponent,
                    th03_opponent_score=(
                        _TH03UnpackScore(round_split.score_p2)
                        if round_split is not None
                        else None
                    ),
                )
            )
    else:
        replay_type = game_ids.ReplayTypes.PVP
        round_split = _TH03LatestRoundSplit(round_splits, 0x0F)
        p1_score = (
            _TH03UnpackScore(round_split.score_p1)
            if round_split is not None
            else final_score
        )
        p2_score = (
            _TH03UnpackScore(round_split.score_p2) if round_split is not None else None
        )

        local_is_p2 = netplay and replay.recorder_role == 2
        local_shot = p2_shot if local_is_p2 else p1_shot
        opponent_shot = p1_shot if local_is_p2 else p2_shot
        local_score = p2_score if local_is_p2 else p1_score
        opponent_score = p1_score if local_is_p2 else p2_score
        local_cpu = replay.is_cpu_p2 if local_is_p2 else replay.is_cpu_p1
        opponent_cpu = replay.is_cpu_p1 if local_is_p2 else replay.is_cpu_p2
        stages.append(
            ReplayStage(
                stage=1,
                score=local_score,
                th03_player_cpu=bool(local_cpu),
                th03_opponent_cpu=bool(opponent_cpu),
                th03_opponent_shot=opponent_shot,
                th03_opponent_score=opponent_score,
            )
        )

        p1_shot = local_shot
        if round_split is not None:
            final_score = local_score

    name = replay.name.decode("ascii").rstrip() if any(replay.name) else ""
    misses = None if replay.final_misses == _TH03_SCORE_UNKNOWN else replay.final_misses
    return ReplayInfo(
        game=game_ids.GameIDs.TH03,
        shot=p1_shot,
        difficulty=replay.rank,
        score=final_score,
        timestamp=_TH03ParseDosDate(replay.dos_date),
        name=name,
        replay_type=replay_type,
        stages=stages,
        slowdown=(
            (replay.summary.slow_frames * 100 / replay.summary.timed_frames)
            if replay.summary.timed_frames
            else None
        ),
        miss_count=misses,
        is_clear=(
            replay.end_reason == _TH03_END_REASON_COMPLETE
            if replay.game_mode == _TH03_GAME_MODE_STORY
            else None
        ),
        th03_ruleset=replay.ruleset,
        th03_is_netplay=netplay,
        th03_recorder_role=replay.recorder_role,
        th03_recorder_source=replay.recorder_source,
        th03_p1_uuid=_TH03Uuid(replay.player_one_uuid),
        th03_p2_uuid=_TH03Uuid(replay.player_two_uuid),
        th03_match_id=_TH03Uuid(replay.match_id),
        th03_p1_name=_TH03FallbackNametag(
            replay.player_one_nametag, replay.player_one_nametag_length
        ),
        th03_p2_name=_TH03FallbackNametag(
            replay.player_two_nametag, replay.player_two_nametag_length
        ),
    )


# piv is stored with extra precision, we trunctate the value to what is shown ingame
def convert_stored_PIV_to_displayed(game_id: str, piv: int) -> int:
    if game_id in ["th12", "th128", "th13", "th14", "th15", "th16", "th17", "th18"]:
        return (math.trunc(piv / 1000)) * 10
    return piv


def _Parse06(rep_raw):
    cryptdata = bytearray(rep_raw[15:])
    td.decrypt06(cryptdata, rep_raw[14])
    replay = th06.Th06.from_bytes(cryptdata)

    shots = ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]

    rep_stages = []

    enumerated_non_dummy_stages = [
        (i, _pointer.body)
        for i, _pointer in enumerate(replay.file_header.stage_offsets)
        if _pointer.body
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

    r_type = game_ids.ReplayTypes.FULL_GAME
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
        (i, _pointer.body)
        for i, _pointer in enumerate(replay.file_header.stage_offsets)
        if _pointer.body
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

    r_type = game_ids.ReplayTypes.FULL_GAME
    if len(rep_stages) == 1 and replay.header.difficulty not in [4, 5]:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    # Touhou 7 does not store the year of the replay, but datetimes requires one.
    # Therefore we set one. It must be a leap year in order for Feb 29 to be valid.
    arbitrary_leap_year = 1904
    timestamp = time.strptime(f"{replay.header.date}/{arbitrary_leap_year}", "%m/%d/%Y")

    r = ReplayInfo(
        game=game_ids.GameIDs.TH07,
        shot=shots[replay.header.shot],
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=timestamp,
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

    #   else full run

    # TH08 stores stage data values from the start of the stage but score from the end
    route = None

    enumerated_non_dummy_stages = [
        (i, _pointer.body)
        for i, _pointer in enumerate(replay.file_header.stage_offsets)
        if _pointer.body
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

    r_type = game_ids.ReplayTypes.FULL_GAME
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
    stage_pointers = replay.file_header.stage_offsets
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
    r_type = game_ids.ReplayTypes.FULL_GAME

    highest_stage = 0
    if not stage_pointers[9].body:
        #  story mode
        #  collect start-of-stage data
        for i in range(9):
            if stage_pointers[i].body:
                #   real stage
                p1 = stage_pointers[i].body
                p2 = stage_pointers[i + 10].body

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
            p1 = stage_pointers[highest_stage].body
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
        p1 = stage_pointers[9].body
        p2 = stage_pointers[19].body

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


def _Parse095(rep_raw):
    encrypted_replay = th095_encrypted.Th095Encrypted.from_bytes(rep_raw)

    if encrypted_replay.userdata.level.value == "EX":
        spell_level = 11
    else:
        spell_level = int(encrypted_replay.userdata.level.value)
    spell_scene = int(encrypted_replay.userdata.scene.value)

    scene_count_per_level = {
        1: 6,
        2: 6,
        3: 8,
        4: 9,
        5: 8,
        6: 8,
        7: 8,
        8: 8,
        9: 8,
        10: 8,
        11: 8,
    }
    if spell_level not in scene_count_per_level:
        raise BadReplayError("Invalid spell level in replay")
    if spell_scene < 1 or spell_scene > scene_count_per_level[spell_level]:
        raise BadReplayError("Invalid spell scene in replay")

    return ReplayInfo(
        game=game_ids.GameIDs.TH095,
        shot="Aya",
        score=int(encrypted_replay.userdata.score.value),
        timestamp=time.strptime(encrypted_replay.userdata.date.value, "%y/%m/%d %H:%M"),
        name=encrypted_replay.userdata.username.value,
        replay_type=game_ids.ReplayTypes.SCENE_GAME,
        scene_game_level=spell_level,
        scene_game_scene=spell_scene,
        slowdown=float(encrypted_replay.userdata.slowdown.value),
    )


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

    r_type = game_ids.ReplayTypes.FULL_GAME
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

    r_type = game_ids.ReplayTypes.FULL_GAME
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
            s.piv = convert_stored_PIV_to_displayed(
                game_ids.GameIDs.TH12, next_stage_start_data.piv
            )
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            #   fix zun fuckery
            if s.life_pieces > 0:
                s.life_pieces -= 1
            s.bombs = next_stage_start_data.bombs
            # For some reason, bomb_pieces ends up being twice its original value.
            s.bomb_pieces = next_stage_start_data.bomb_pieces / 2
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.FULL_GAME
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


def _Parse128(rep_raw):
    header = th_modern.ThModern.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x800, 0x5E, 0xE7)
    td.decrypt(comp_data, 0x80, 0x7D, 0x36)
    replay = th128.Th128.from_bytes(td.unlzss(comp_data))

    routes = [
        "A-1",
        "A-2",
        "B-1",
        "B-2",
        "C-1",
        "C-2",
    ]

    rep_stages = []

    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score * 10
            s.graze = next_stage_start_data.graze
            s.th128_motivation = next_stage_start_data.motivation
            s.th128_perfect_freeze = next_stage_start_data.perfect_freeze
            s.th128_frozen_area = next_stage_start_data.frozen_area
        else:
            s.score = replay.header.score * 10
        rep_stages.append(s)

    return ReplayInfo(
        game=game_ids.GameIDs.TH128,
        route=routes[replay.header.route] if replay.header.route != 6 else None,
        shot="Cirno",
        replay_type=game_ids.ReplayTypes.FULL_GAME,
        name=replay.header.name.replace("\x00", ""),
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        score=replay.header.score * 10,
        slowdown=replay.header.slowdown,
        difficulty=replay.header.difficulty,
        stages=rep_stages,
    )


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
    for current_stage, next_stage in zip(replay.stages, replay.stages[1:] + [None]):
        s = ReplayStage(stage=current_stage.stage_num, score=replay.header.score * 10)
        if next_stage is not None:
            s.score = next_stage.score * 10
            s.power = next_stage.power
            # piv is stored with extra precision, we trunctate the value to what is shown ingame
            s.piv = convert_stored_PIV_to_displayed(
                game_ids.GameIDs.TH13, next_stage.piv
            )
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

    r_type = game_ids.ReplayTypes.FULL_GAME
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
            s.piv = convert_stored_PIV_to_displayed(
                game_ids.GameIDs.TH14, next_stage_start_data.piv
            )
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            s.bombs = next_stage_start_data.bombs
            s.bomb_pieces = next_stage_start_data.bomb_pieces
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.FULL_GAME
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
            s.piv = convert_stored_PIV_to_displayed(
                game_ids.GameIDs.TH15, next_stage_start_data.piv
            )
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            s.bombs = next_stage_start_data.bombs
            s.bomb_pieces = next_stage_start_data.bomb_pieces
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.FULL_GAME
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
            s.piv = convert_stored_PIV_to_displayed(
                game_ids.GameIDs.TH16, next_stage_start_data.piv
            )
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

    r_type = game_ids.ReplayTypes.FULL_GAME
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
            s.piv = convert_stored_PIV_to_displayed(
                game_ids.GameIDs.TH17, next_stage_start_data.piv
            )
            s.lives = next_stage_start_data.lives
            s.life_pieces = next_stage_start_data.life_pieces
            s.bombs = next_stage_start_data.bombs
            s.bomb_pieces = next_stage_start_data.bomb_pieces
            s.graze = next_stage_start_data.graze
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score * 10
        rep_stages.append(s)

    r_type = game_ids.ReplayTypes.FULL_GAME
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
            piv=convert_stored_PIV_to_displayed(
                game_ids.GameIDs.TH18, current_stage_end_data.piv
            ),
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

    r_type = game_ids.ReplayTypes.FULL_GAME
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


def _20SubshotToStone(stone_id: int) -> str:
    return [
        "Red",
        "Red2",
        "Blue",
        "Blue2",
        "Yellow",
        "Yellow2",
        "Green",
        "Green2",
        "Common",
    ][stone_id]


def _Parse20(rep_raw) -> ReplayInfo:
    header = th_modern_20_header.ThModern20Header.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0x5C, 0xE1)
    td.decrypt(comp_data, 0x100, 0x7D, 0x3A)
    decomp = td.unlzss(comp_data)

    replay = th20.Th20.from_bytes(decomp)
    character = ["Reimu", "Marisa"][replay.header.shot]
    stones = [_20SubshotToStone(stone_id) for stone_id in replay.header.stones]
    shot = character + stones[0]

    if _is_spell_practice_modern(replay.header):
        raise Exception("Spell practice is not yet supported")

    # No stage practice support yet.

    r_type = game_ids.ReplayTypes.FULL_GAME
    if replay.header.stage_count == 1 and replay.header.difficulty != 4:
        r_type = game_ids.ReplayTypes.STAGE_PRACTICE

    r = ReplayInfo(
        game=game_ids.GameIDs.TH20,
        shot=shot,
        equipment=stones,
        difficulty=replay.header.difficulty,
        score=replay.header.score * 10,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=r_type,
    )

    return r


def _ParseAlco(rep_raw) -> ReplayInfo:
    header = alco_userdata.AlcoUserdata.from_bytes(rep_raw)
    comp_data = bytearray(header.main.comp_data)

    td.decrypt(comp_data, 0x400, 0xAA, 0xE1)
    td.decrypt(comp_data, 0x80, 0x3D, 0x7A)
    replay = alco.Alco.from_bytes(td.unlzss(comp_data))

    rep_stages = []

    for current_stage_start_data, next_stage_start_data in zip(
        replay.stages, replay.stages[1:] + [None]
    ):
        s = ReplayStage(
            stage=current_stage_start_data.stage_num,
        )
        if next_stage_start_data is not None:
            s.score = next_stage_start_data.score
        else:
            # no next stage means this is the last stage, so use the final run score
            s.score = replay.header.score
        rep_stages.append(s)

    r = ReplayInfo(
        game=game_ids.GameIDs.ALCO,
        shot="Isami",
        score=replay.header.score,
        timestamp=datetime.datetime.fromtimestamp(
            replay.header.timestamp, tz=datetime.timezone.utc
        ),
        name=replay.header.name.replace("\x00", ""),
        slowdown=replay.header.slowdown,
        replay_type=game_ids.ReplayTypes.FULL_GAME,
        stages=rep_stages,
    )

    return r


def _DetermineTH13orTH14(replay):
    # thank you ZUN
    # yes, one of the only indications of which game a replay is from here is from a USERDATA string
    header = th_modern.ThModern.from_bytes(replay)
    # royalflare corrupts some of the userdata, and since the userdata is the only way to determine between TH13 and TH14
    # we have to just keep finding new replays with fucked strings and adding them to these checks
    if header.userdata.user_desc[4] in [0x90, 0xC9]:
        # the shift-jis character is 廟
        return _Parse13(replay)
    elif header.userdata.user_desc[4] in [0x8B, 0xBB]:
        # the shift-jis character is 城
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
        if gamecode == b"T3RP":
            return _Parse03(replay)
        elif gamecode == b"T6RP":
            return _Parse06(replay)
        elif gamecode == b"T7RP":
            return _Parse07(replay)
        elif gamecode == b"T8RP":
            return _Parse08(replay)
        elif gamecode == b"T9RP":
            return _Parse09(replay)
        elif gamecode == b"t95r":
            return _Parse095(replay)
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
        elif gamecode == b"t20r":
            return _Parse20(replay)
        elif gamecode == b"128r":
            return _Parse128(replay)
        elif gamecode == b"al1r":
            return _ParseAlco(replay)
        else:
            logging.warning("Failed to comprehend gamecode %s", str(gamecode))
            raise UnsupportedGameError("This game is unsupported.")
    except (ValueError, IndexError, EOFError, KaitaiStructError):
        raise BadReplayError("This replay is corrupted or otherwise malformed")
