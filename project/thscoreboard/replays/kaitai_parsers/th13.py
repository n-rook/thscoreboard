# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th13(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Th13.Header(self._io, self, self._root)
        self.stages = [None] * (self.header.stage_count)
        for i in range(self.header.stage_count):
            self.stages[i] = Th13.Stage(self._io, self, self._root)


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
            self.unknown = self._io.read_bytes(60)
            self.slowdown = self._io.read_f4le()
            self.stage_count = self._io.read_u4le()
            self.shot = self._io.read_u4le()
            self.subshot_unused = self._io.read_u4le()
            self.difficulty = self._io.read_u4le()
            self.cleared = self._io.read_u4le()
            self.unused = self._io.read_bytes(4)
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
            self.subshot_unused = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.unknown = self._io.read_u4le()
            self.continues = self._io.read_u4le()
            self.unknown2 = self._io.read_u4le()
            self.graze = self._io.read_u4le()
            self.unknown3 = self._io.read_u4le()
            self.unknown4 = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.piv_min = self._io.read_u4le()
            self.piv_max = self._io.read_u4le()
            self.power = self._io.read_u4le()
            self.power_max = self._io.read_u4le()
            self.power_min = self._io.read_u4le()
            self.lives = self._io.read_u4le()
            self.life_pieces = self._io.read_u4le()
            self.extends = self._io.read_u4le()
            self.bombs = self._io.read_u4le()
            self.bomb_pieces = self._io.read_u4le()
            self.trance = self._io.read_u4le()
            self.unknown5 = self._io.read_u4le()
            self.focused = self._io.read_u4le()
            self.spellcard_real_times = [None] * (21)
            for i in range(21):
                self.spellcard_real_times[i] = self._io.read_u4le()

            self.stage_data = self._io.read_bytes(self.end_off)



