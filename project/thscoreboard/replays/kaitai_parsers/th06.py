# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th06(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.file_header = Th06.FileHeader(self._io, self, self._root)

    class Dummy(KaitaiStruct):
        """blank type."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_2 = self._io.read_u1()
            self.date = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"SJIS")
            self.unknown_3 = self._io.read_u2le()
            self.score = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()
            self.slowdown = self._io.read_f4le()
            self.unknown_5 = self._io.read_u4le()
            self.stage_offsets = []
            for i in range(7):
                self.stage_offsets.append(Th06.StagePointer(self._io, self, self._root))



    class StagePointer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.raw_offset = self._io.read_u4le()

        @property
        def offset(self):
            """Offset relative to decrypted file."""
            if hasattr(self, '_m_offset'):
                return self._m_offset

            self._m_offset = (self.raw_offset - 15)
            return getattr(self, '_m_offset', None)

        @property
        def body(self):
            if hasattr(self, '_m_body'):
                return self._m_body

            if self.raw_offset != 0:
                _pos = self._io.pos()
                self._io.seek(self.offset)
                self._m_body = Th06.Stage(self._io, self, self._root)
                self._io.seek(_pos)

            return getattr(self, '_m_body', None)


    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.score = self._io.read_u4le()
            self.seed = self._io.read_u2le()
            self.unknown_1 = self._io.read_u2le()
            self.power = self._io.read_u1()
            self.lives = self._io.read_s1()
            self.bombs = self._io.read_s1()
            self.rank = self._io.read_u1()



