# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th09(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.file_header = Th09.FileHeader(self._io, self, self._root)
        self.header = Th09.Header(self._io, self, self._root)

    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x54\x39\x52\x50":
                raise kaitaistruct.ValidationNotEqualError(b"\x54\x39\x52\x50", self.magic, self._io, u"/types/file_header/seq/0")
            self.version = self._io.read_u2le()
            self.unknown_1 = self._io.read_bytes(6)
            self.comp_size = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.key = self._io.read_u1()
            self.unknown_3 = self._io.read_bytes(7)
            self.decomp_size = self._io.read_u4le()
            self.stage_offsets = []
            for i in range(20):
                self.stage_offsets.append(Th09.StagePointer(self._io, self, self._root))

            self.unknown_offsets = []
            for i in range(20):
                self.unknown_offsets.append(self._io.read_u4le())



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_1 = self._io.read_u4le()
            self.date = (KaitaiStream.bytes_terminate(self._io.read_bytes(10), 0, False)).decode(u"ASCII")
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"SJIS")
            self.difficulty = self._io.read_u1()


    class StagePointer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()

        @property
        def body(self):
            if hasattr(self, '_m_body'):
                return self._m_body

            if self.offset != 0:
                _pos = self._io.pos()
                self._io.seek(self.offset)
                self._m_body = Th09.Stage(self._io, self, self._root)
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
            self.pair = self._io.read_u2le()
            self.shot = self._io.read_u1()
            self.ai = self._io.read_bits_int_be(1) != 0
            self._io.align_to_byte()
            self.lives = self._io.read_u1()
            self.unknown = self._io.read_u1()



