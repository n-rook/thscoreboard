# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th06(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Th06, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.file_header = Th06.FileHeader(self._io, self, self._root)


    def _fetch_instances(self):
        pass
        self.file_header._fetch_instances()

    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th06.FileHeader, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.unknown_2 = self._io.read_u1()
            self.date = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"Shift_JIS")
            self.unknown_3 = self._io.read_u2le()
            self.score = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()
            self.slowdown = self._io.read_f4le()
            self.unknown_5 = self._io.read_u4le()
            self.stage_offsets = []
            for i in range(7):
                self.stage_offsets.append(Th06.StagePointer(self._io, self, self._root))



        def _fetch_instances(self):
            pass
            for i in range(len(self.stage_offsets)):
                pass
                self.stage_offsets[i]._fetch_instances()



    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th06.Stage, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.score = self._io.read_u4le()
            self.seed = self._io.read_u2le()
            self.unknown_1 = self._io.read_u2le()
            self.power = self._io.read_u1()
            self.lives = self._io.read_s1()
            self.bombs = self._io.read_s1()
            self.rank = self._io.read_u1()


        def _fetch_instances(self):
            pass


    class StagePointer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th06.StagePointer, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.raw_offset = self._io.read_u4le()


        def _fetch_instances(self):
            pass
            _ = self.body
            if hasattr(self, '_m_body'):
                pass
                self._m_body._fetch_instances()


        @property
        def body(self):
            if hasattr(self, '_m_body'):
                return self._m_body

            if self.raw_offset != 0:
                pass
                _pos = self._io.pos()
                self._io.seek(self.offset)
                self._m_body = Th06.Stage(self._io, self, self._root)
                self._io.seek(_pos)

            return getattr(self, '_m_body', None)

        @property
        def offset(self):
            """Offset relative to decrypted file."""
            if hasattr(self, '_m_offset'):
                return self._m_offset

            self._m_offset = self.raw_offset - 15
            return getattr(self, '_m_offset', None)



