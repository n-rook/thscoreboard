# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th07(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.file_header = Th07.FileHeader(self._io, self, self._root)
        self.header = Th07.Header(self._io, self, self._root)

    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x54\x37\x52\x50":
                raise kaitaistruct.ValidationNotEqualError(b"\x54\x37\x52\x50", self.magic, self._io, u"/types/file_header/seq/0")
            self.version = self._io.read_bytes(2)
            self.unknown_1 = self._io.read_bytes(7)
            self.key = self._io.read_u1()
            self.unknown_2 = self._io.read_u2le()
            self.unknown_3 = self._io.read_u4le()
            self.comp_size = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.stage_offsets = []
            for i in range(7):
                self.stage_offsets.append(Th07.StagePointer(self._io, self, self._root))

            self.unknown_4 = []
            for i in range(7):
                self.unknown_4.append(self._io.read_u4le())



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_1 = self._io.read_bytes(2)
            self.shot = self._io.read_u1()
            self.difficulty = self._io.read_u1()
            self.date = (KaitaiStream.bytes_terminate(self._io.read_bytes(6), 0, False)).decode(u"ASCII")
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"SJIS")
            self.unknown_2 = self._io.read_bytes(5)
            self.score = self._io.read_u4le()
            self.unknown_3 = []
            for i in range(23):
                self.unknown_3.append(self._io.read_u4le())

            self.slowdown = self._io.read_f4le()


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
                self._m_body = Th07.Stage(self._io, self, self._root)
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
            self.point_items = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.cherrymax = self._io.read_u4le()
            self.cherry = self._io.read_u4le()
            self.graze = self._io.read_u4le()
            self.unknown_1 = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.unknown_3 = self._io.read_u2le()
            self.power = self._io.read_u1()
            self.lives = self._io.read_u1()
            self.bombs = self._io.read_u1()
            self.unknown_4 = self._io.read_u1()



