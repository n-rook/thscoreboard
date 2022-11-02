# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th11(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Th11.Header(self._io, self, self._root)
        self.stages = [None] * (self.header.stagecount)
        for i in range(self.header.stagecount):
            self.stages[i] = Th11.Stage(self._io, self, self._root)


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
            self.unknown_1 = self._io.read_bytes(60)
            self.slowdown = self._io.read_f4le()
            self.stagecount = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.shot = self._io.read_u4le()
            self.difficulty = self._io.read_u4le()
            self.unknown_3 = self._io.read_bytes(8)


    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.stage = self._io.read_u2le()
            self.seed = self._io.read_u2le()
            self.ignore = self._io.read_u4le()
            self.stage_size = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.power = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.lives = self._io.read_u2le()
            self.life_pieces = self._io.read_u2le()
            self.unknown_1 = self._io.read_bytes(24)
            self.graze = self._io.read_u4le()
            self.unknown_2 = self._io.read_bytes(88)
            self.stage_data = self._io.read_bytes(self.stage_size)



