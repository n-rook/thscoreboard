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
            self.padding = self._io.read_bytes(32)
            self.stage_offsets = []
            for i in range(40):
                self.stage_offsets.append(self._io.read_u4le())



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_1 = self._io.read_u4le()
            self.date = (KaitaiStream.bytes_terminate(self._io.read_bytes(10), 0, False)).decode(u"ASCII")
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.difficulty = self._io.read_u1()


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


    @property
    def stages(self):
        if hasattr(self, '_m_stages'):
            return self._m_stages

        _pos = self._io.pos()
        self._m_stages = []
        for i in range(40):
            _on = self.file_header.stage_offsets[i]
            if _on == 0:
                self._m_stages.append(Th09.Dummy(self._io, self, self._root))
            else:
                #   kaitai bug fix: move this line to this else section
                self._io.seek(self.file_header.stage_offsets[i])
                self._m_stages.append(Th09.Stage(self._io, self, self._root))

        self._io.seek(_pos)
        return getattr(self, '_m_stages', None)


