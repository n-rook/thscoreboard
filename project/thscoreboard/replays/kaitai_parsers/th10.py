# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th10(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Th10, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.header = Th10.Header(self._io, self, self._root)
        self.stages = []
        for i in range(self.header.stagecount):
            self.stages.append(Th10.Stage(self._io, self, self._root))



    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        for i in range(len(self.stages)):
            pass
            self.stages[i]._fetch_instances()


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th10.Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes(12)).decode(u"Shift_JIS")
            self.timestamp = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(52)
            self.slowdown = self._io.read_f4le()
            self.stagecount = self._io.read_u4le()
            self.shot = self._io.read_u4le()
            self.subshot = self._io.read_u4le()
            self.difficulty = self._io.read_u4le()
            self.unknown_3 = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()


        def _fetch_instances(self):
            pass


    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th10.Stage, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.stage_num = self._io.read_u2le()
            self.unknown_1 = self._io.read_u2le()
            self.unknown_2 = self._io.read_u4le()
            self.len_stage_data = self._io.read_u4le()
            self.score = self._io.read_u4le()
            self.power = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.unknown_3 = self._io.read_u4le()
            self.lives = self._io.read_u4le()
            self.rest_of_header = self._io.read_bytes(420)
            self.stage_data = self._io.read_bytes(self.len_stage_data)


        def _fetch_instances(self):
            pass



