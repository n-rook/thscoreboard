# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th20(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Th20, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.header = Th20.Header(self._io, self, self._root)


    def _fetch_instances(self):
        pass
        self.header._fetch_instances()

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th20.Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(16), 0, False)).decode(u"Shift_JIS")
            self.timestamp = self._io.read_u8le()
            self.score = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(180)
            self.slowdown = self._io.read_f4le()
            self.stage_count = self._io.read_u4le()
            self.shot = self._io.read_u4le()
            self.stones = []
            for i in range(4):
                self.stones.append(self._io.read_u4le())

            self.unknown_2 = self._io.read_bytes(4)
            self.difficulty = self._io.read_u4le()
            self.unknown_3 = self._io.read_bytes(4)
            self.unknown_4 = self._io.read_bytes(4)
            self.spell_practice_id = self._io.read_u4le()


        def _fetch_instances(self):
            pass
            for i in range(len(self.stones)):
                pass




