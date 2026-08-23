# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th03V14(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(8)
        if not self.magic == b"\x54\x33\x52\x50\x4C\x59\x31\x34":
            raise kaitaistruct.ValidationNotEqualError(b"\x54\x33\x52\x50\x4C\x59\x31\x34", self.magic, self._io, u"/seq/0")
        self.version = self._io.read_u2le()
        if not self.version == 14:
            raise kaitaistruct.ValidationNotEqualError(14, self.version, self._io, u"/seq/1")
        self.header_size = self._io.read_u2le()
        if not self.header_size == 896:
            raise kaitaistruct.ValidationNotEqualError(896, self.header_size, self._io, u"/seq/2")
        self.sample_size = self._io.read_u2le()
        if not self.sample_size == 0:
            raise kaitaistruct.ValidationNotEqualError(0, self.sample_size, self._io, u"/seq/3")
        self.flags = self._io.read_u2le()
        self.status = self._io.read_u1()
        self.end_reason = self._io.read_u1()
        self.game_mode = self._io.read_u1()
        self.rank = self._io.read_u1()
        self.key_mode = self._io.read_u1()
        self.playchar_p1 = self._io.read_u1()
        self.playchar_p2 = self._io.read_u1()
        self.story_stage = self._io.read_u1()
        self.is_cpu_p1 = self._io.read_u1()
        self.is_cpu_p2 = self._io.read_u1()
        self.sample_count = self._io.read_u4le()
        self.final_frame_count = self._io.read_u4le()
        self.resident_rand = self._io.read_u4le()
        self.random_seed_snapshot = self._io.read_u4le()
        self.input_offset = self._io.read_u4le()
        self.input_size = self._io.read_u4le()
        self.snapshot_offset = self._io.read_u4le()
        if not self.snapshot_offset == 896:
            raise kaitaistruct.ValidationNotEqualError(896, self.snapshot_offset, self._io, u"/seq/21")
        self.snapshot_size = self._io.read_u4le()
        if not self.snapshot_size == 289:
            raise kaitaistruct.ValidationNotEqualError(289, self.snapshot_size, self._io, u"/seq/22")
        self.summary_flags = self._io.read_u2le()
        self.final_route = self._io.read_u1()
        self.final_game_mode = self._io.read_u1()
        self.final_story_stage = self._io.read_u1()
        self.final_round_id = self._io.read_u1()
        self.final_winner = self._io.read_u1()
        self.final_story_lives = self._io.read_u1()
        self.final_misses = self._io.read_u1()
        self.stage_reached_count = self._io.read_u1()
        if (self.flags & 4) == 0:
            self.story = Th03V14.StorySummary(self._io, self, self._root)

        if (self.flags & 4) != 0:
            self.practice = Th03V14.PracticeSummary(self._io, self, self._root)

        self.final_score = Th03V14.PackedScore(self._io, self, self._root)
        self.autofire = self._io.read_u1()
        self.dos_date = self._io.read_u2le()
        self.name = self._io.read_bytes(8)
        self.summary = Th03V14.SummaryExtension(self._io, self, self._root)
        self.ruleset = self._io.read_u1()
        self.recording_flags = self._io.read_u1()
        self.recorder_role = self._io.read_u1()
        self.recorder_source = self._io.read_u1()
        self.player_one_uuid = self._io.read_bytes(16)
        self.player_two_uuid = self._io.read_bytes(16)
        self.match_id = self._io.read_bytes(16)
        self.player_one_nametag_length = self._io.read_u1()
        if not self.player_one_nametag_length <= 57:
            raise kaitaistruct.ValidationGreaterThanError(57, self.player_one_nametag_length, self._io, u"/seq/46")
        self.player_two_nametag_length = self._io.read_u1()
        if not self.player_two_nametag_length <= 57:
            raise kaitaistruct.ValidationGreaterThanError(57, self.player_two_nametag_length, self._io, u"/seq/47")
        self.player_one_nametag = self._io.read_bytes(57)
        self.player_two_nametag = self._io.read_bytes(57)
        self.identity_reserved = self._io.read_bytes(106)
        self.checkpoints = []
        for i in range((self.input_offset - self.header_size) // self.snapshot_size):
            self.checkpoints.append(Th03V14.Checkpoint(self._io, self, self._root))

        self.input = self._io.read_bytes(self.input_size)

    class RoundSplit(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.stage_round = self._io.read_u1()
            self.route_winner = self._io.read_u1()
            self.score_p1 = Th03V14.PackedScore(self._io, self, self._root)
            self.score_p2 = Th03V14.PackedScore(self._io, self, self._root)
            self.real_frames = self._io.read_u4le()


    class CompactSnapshot(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.resident_rand = self._io.read_u4le()
            self.random_seed_snapshot = self._io.read_u4le()
            self.rank = self._io.read_u1()
            self.key_mode = self._io.read_u1()
            self.game_mode = self._io.read_u1()
            self.story_stage = self._io.read_u1()
            self.story_lives = self._io.read_u1()
            self.rem_credits = self._io.read_u1()
            self.skill = self._io.read_u1()
            self.demo_num = self._io.read_u1()
            self.pid_winner = self._io.read_u1()
            self.show_score_menu = self._io.read_u1()
            self.op_animation_fast = self._io.read_u1()
            self.is_cpu = []
            for i in range(2):
                self.is_cpu.append(self._io.read_u1())

            self.playchar_paletted = []
            for i in range(2):
                self.playchar_paletted.append(self._io.read_u1())

            self.story_opponents = []
            for i in range(9):
                self.story_opponents.append(self._io.read_u1())

            self.score_last = []
            for i in range(2):
                self.score_last.append(Th03V14.UnpackedScore(self._io, self, self._root))

            self.autofire = self._io.read_u1()
            self.player_runtime = self._io.read_bytes(30)
            self.round_reset_seed = self._io.read_u4le()
            self.formation_first = self._io.read_u1()


    class PracticeSummary(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.preset = self._io.read_u1()
            self.stage = self._io.read_u1()
            self.round = self._io.read_u1()
            self.stock = self._io.read_u1()
            self.extends_gained = self._io.read_u1()
            self.cpu_timer = self._io.read_u1()
            self.round_speed = self._io.read_u1()
            self.bullet_speed = self._io.read_u1()
            self.p1_spell = self._io.read_u1()
            self.cpu_spell = self._io.read_u1()
            self.boss_level = self._io.read_u1()
            self.cpu_damage = self._io.read_u1()
            self.initial_cpu_safety_frames = self._io.read_u2le()
            self.p1_gauge = self._io.read_u1()
            self.cpu_gauge = self._io.read_u1()
            self.reserved = self._io.read_bytes(29)


    class UnpackedScore(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.digits = self._io.read_bytes(8)


    class PackedScore(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.digits = self._io.read_bytes(4)


    class StageClearBonus(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.total = Th03V14.PackedScore(self._io, self, self._root)
            self.max_combo = self._io.read_u1()
            self.gauge_attacks = self._io.read_u1()
            self.boss_attacks = self._io.read_u1()
            self.boss_reversals = self._io.read_u1()
            self.boss_panics = self._io.read_u1()
            self.remaining_lives = self._io.read_u1()


    class StorySummary(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.stage_opponents = []
            for i in range(9):
                self.stage_opponents.append(self._io.read_u1())

            self.stage_scores = []
            for i in range(9):
                self.stage_scores.append(Th03V14.PackedScore(self._io, self, self._root))



    class RoundState(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.round_id = self._io.read_u1()
            self.rounds_won = []
            for i in range(2):
                self.rounds_won.append(self._io.read_u1())

            self.score = []
            for i in range(2):
                self.score.append(Th03V14.UnpackedScore(self._io, self, self._root))

            self.round_speed = self._io.read_u1()
            self.bullet_speed = self._io.read_u1()
            self.spell_rank = []
            for i in range(2):
                self.spell_rank.append(self._io.read_u1())

            self.boss_rank = self._io.read_u1()
            self.cpu_damage = self._io.read_u1()
            self.extends_gained = self._io.read_u1()
            self.cpu_safety_frames = []
            for i in range(2):
                self.cpu_safety_frames.append(self._io.read_u2le())



    class Checkpoint(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sample_count = self._io.read_u4le()
            self.global_frame = self._io.read_u4le()
            self.input_size = self._io.read_u4le()
            self.snapshot = Th03V14.CompactSnapshot(self._io, self, self._root)
            self.round_state = Th03V14.RoundState(self._io, self, self._root)
            self.round_carry = self._io.read_bytes(163)


    class SummaryExtension(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.flags = self._io.read_u1()
            self.round_reached_count = self._io.read_u1()
            self.round_splits = []
            for i in range(27):
                self.round_splits.append(Th03V14.RoundSplit(self._io, self, self._root))

            self.stage_clear_bonuses = []
            for i in range(9):
                self.stage_clear_bonuses.append(Th03V14.StageClearBonus(self._io, self, self._root))

            self.timed_frames = self._io.read_u4le()
            self.slow_frames = self._io.read_u4le()
            self.checkpoint_count = self._io.read_u1()
            self.checkpoint_stage_round = []
            for i in range(15):
                self.checkpoint_stage_round.append(self._io.read_u1())
