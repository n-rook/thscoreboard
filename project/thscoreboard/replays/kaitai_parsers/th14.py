# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th14(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Th14.Header(self._io, self, self._root)
        self.stages = [None] * (self.header.stage_count)
        for i in range(self.header.stage_count):
            self.stages[i] = Th14.Stage(self._io, self, self._root)


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(12), 0, False)).decode(u"ASCII")
            self.timestamp = self._io.read_u8le()
            self.score = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(92)
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
            self.shot = self._io.read_u4le()
            self.subshot = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.difficulty = self._io.read_u4le()
            self.continues = self._io.read_u4le()
            self.unknown_1 = self._io.read_u4le()
            self.graze = self._io.read_u4le()
            self.spell_practice_id = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.piv_min = self._io.read_u4le()
            self.piv_max = self._io.read_u4le()
            self.power = self._io.read_u4le()
            self.power_max = self._io.read_u4le()
            self.power_levelup = self._io.read_u4le()
            self.lives = self._io.read_u4le()
            self.life_pieces = self._io.read_u4le()
            self.unknown_3 = self._io.read_u4le()
            self.bombs = self._io.read_u4le()
            self.bomb_pieces = self._io.read_u4le()
            self.score_from_poc = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()
            self.unknown_5 = self._io.read_u4le()
            self.unknown_6 = self._io.read_u4le()
            self.last_item_collected_pos = [None] * (3)
            for i in range(3):
                self.last_item_collected_pos[i] = self._io.read_f4le()

            self.poc_count = self._io.read_u4le()
            self.focused = self._io.read_u4le()
            self.spellcard_real_times = [None] * (21)
            for i in range(21):
                self.spellcard_real_times[i] = self._io.read_u4le()

            self.stage_data = self._io.read_bytes(self.end_off)



