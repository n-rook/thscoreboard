# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th17(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Th17.Header(self._io, self, self._root)
        self.stages = []
        for i in range(self.header.stage_count):
            self.stages.append(Th17.Stage(self._io, self, self._root))


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(16), 0, False)).decode(u"ASCII")
            self.timestamp = self._io.read_u8le()
            self.score = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(100)
            self.slowdown = self._io.read_f4le()
            self.stage_count = self._io.read_u4le()
            self.shot = self._io.read_u4le()
            self.subshot = self._io.read_u4le()
            self.difficulty = self._io.read_u4le()
            self.cleared = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.spell_practice_id = self._io.read_u4le()


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
            self.stage_num_2 = self._io.read_u4le()
            self.stage_num_3 = self._io.read_u4le()
            self.chapter = self._io.read_u4le()
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
            self.unknown_1 = self._io.read_u4le()
            self.spell_practice_id = self._io.read_u4le()
            self.miss_count = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.point_items_collected = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.piv_min = self._io.read_u4le()
            self.piv_max = self._io.read_u4le()
            self.power = self._io.read_u4le()
            self.power_max = self._io.read_u4le()
            self.power_levelup = self._io.read_u4le()
            self.unknown_3 = self._io.read_u4le()
            self.lives = self._io.read_u4le()
            self.life_pieces = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()
            self.bombs = self._io.read_u4le()
            self.bomb_pieces = self._io.read_u4le()
            self.bomb_restock_on_death = self._io.read_u4le()
            self.unknown_5 = self._io.read_u4le()
            self.unknown_6 = self._io.read_u4le()
            self.hyper_fill = self._io.read_u4le()
            self.tokens = []
            for i in range(5):
                self.tokens.append(self._io.read_u4le())

            self.unknown_7 = []
            for i in range(6):
                self.unknown_7.append(self._io.read_u4le())

            self.unknown_timer = Th17.Timer(self._io, self, self._root)
            self.hyper_time = Th17.Timer(self._io, self, self._root)
            self.unknown_8 = []
            for i in range(3):
                self.unknown_8.append(self._io.read_u4le())

            self.hyper_flags = self._io.read_u4le()
            self.player_is_focused = self._io.read_u4le()
            self.spellcard_real_times = []
            for i in range(21):
                self.spellcard_real_times.append(self._io.read_u4le())

            self.stage_data = self._io.read_bytes(self.end_off)


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



