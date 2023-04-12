# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th18(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Th18.Header(self._io, self, self._root)
        self.stages = []
        for i in range(self.header.stage_count):
            self.stages.append(Th18.Stage(self._io, self, self._root))


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(16), 0, False)).decode(u"SJIS")
            self.timestamp = self._io.read_u8le()
            self.score = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(136)
            self.slowdown = self._io.read_f4le()
            self.stage_count = self._io.read_u4le()
            self.shot = self._io.read_u4le()
            self.subshot_unused = self._io.read_u4le()
            self.difficulty = self._io.read_u4le()
            self.cleared = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.spell_practice_id = self._io.read_u4le()
            self.unknown_3 = self._io.read_u4le()


    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.stage_num = self._io.read_u2le()
            self.rng = self._io.read_u2le()
            self.frame_count = self._io.read_u4le()
            self.end_off = self._io.read_u4le()
            self.pos_subpixel_x = self._io.read_u4le()
            self.pos_subpixel_y = self._io.read_u4le()
            self.player_is_focused_start = self._io.read_u4le()
            self.spellcard_real_times = []
            for i in range(20):
                self.spellcard_real_times.append(self._io.read_u4le())

            self.stage_data_start = Th18.StageData(self._io, self, self._root)
            self.stage_data_end = Th18.StageData(self._io, self, self._root)
            self.player_is_focused_end = self._io.read_u4le()
            self.stage_data = self._io.read_bytes(self.end_off)


    class StageData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.stage_num_2 = self._io.read_u4le()
            self.stage_num_3 = self._io.read_u4le()
            self.unknown_1 = self._io.read_u4le()
            self.time_in_stage = []
            for i in range(3):
                self.time_in_stage.append(self._io.read_u4le())

            self.shot = self._io.read_u4le()
            self.subshot = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.difficulty = self._io.read_u4le()
            self.continues = self._io.read_u4le()
            self.rank_unused = self._io.read_u4le()
            self.graze = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.spell_practice_id = self._io.read_u4le()
            self.miss_count = self._io.read_u4le()
            self.unknown_3 = self._io.read_u4le()
            self.money_collected = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.piv_min = self._io.read_u4le()
            self.piv_max = self._io.read_u4le()
            self.unknown_4 = self._io.read_bytes(8)
            self.power = self._io.read_u4le()
            self.power_max = self._io.read_u4le()
            self.power_levelup = self._io.read_u4le()
            self.unknown_5 = self._io.read_u4le()
            self.lives = self._io.read_u4le()
            self.life_pieces = self._io.read_u4le()
            self.unknown_6 = self._io.read_u4le()
            self.unknown_7 = self._io.read_u4le()
            self.bombs = self._io.read_u4le()
            self.bomb_pieces = self._io.read_u4le()
            self.bomb_restock_on_death = self._io.read_u4le()
            self.unknown_8 = self._io.read_bytes(72)
            self.unknown_9 = Th18.Timer(self._io, self, self._root)
            self.unknown_10 = Th18.Timer(self._io, self, self._root)
            self.unknown_11 = self._io.read_u4le()
            self.cards = []
            for i in range(256):
                self.cards.append(self._io.read_u4le())

            self.cards_param = []
            for i in range(256):
                self.cards_param.append(self._io.read_u4le())

            self.card_active = self._io.read_u4le()


    class Timer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.prev_time = self._io.read_u4le()
            self.time = self._io.read_u4le()
            self.time_f = self._io.read_f4le()
            self.game_speed_ununsed = self._io.read_u4le()
            self.control = self._io.read_u4le()



