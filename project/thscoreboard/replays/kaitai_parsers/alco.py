# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Alco(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Alco.Header(self._io, self, self._root)
        self.stages = []
        for i in range(self.header.stagecount):
            self.stages.append(Alco.Stage(self._io, self, self._root))


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes(12)).decode(u"SJIS")
            self.timestamp = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(52)
            self.slowdown = self._io.read_f4le()
            self.stagecount = self._io.read_u4le()
            self.unknown_2 = self._io.read_bytes(16)


    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.stage_num = self._io.read_u2le()
            self.unknown_1 = self._io.read_bytes(6)
            self.len_stage_data = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.unknown_2 = self._io.read_bytes(8)
            self.stage_data = self._io.read_bytes(self.len_stage_data)



