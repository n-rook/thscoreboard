# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th128(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Th128.Header(self._io, self, self._root)
        self.stages = []
        for i in range(self.header.stagecount):
            self.stages.append(Th128.Stage(self._io, self, self._root))


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(12), 0, False)).decode(u"SJIS")
            self.timestamp = self._io.read_u8le()
            self.score = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(60)
            self.slowdown = self._io.read_f4le()
            self.stagecount = self._io.read_u4le()
            self.route = self._io.read_u4le()
            self.subshot_unused = self._io.read_u4le()
            self.difficulty = self._io.read_u4le()
            self.cleared = self._io.read_u4le()
            self.unknown_2 = self._io.read_bytes(4)


    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.stage = self._io.read_u2le()
            self.seed = self._io.read_u2le()
            self.frames = self._io.read_u4le()
            self.stage_size = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.unknown_0 = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(8)
            self.continues = self._io.read_u4le()
            self.unknown_2 = self._io.read_bytes(4)
            self.graze = self._io.read_u4le()
            self.unknown_3 = self._io.read_bytes(84)
            self.motivation = self._io.read_u4le()
            self.perfect_freeze = self._io.read_u4le()
            self.frozen_area = self._io.read_f4le()
            self.unused_1 = self._io.read_bytes(4)
            self.stage_data = self._io.read_bytes(self.stage_size)



