# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th08(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.file_header = Th08.FileHeader(self._io, self, self._root)
        self.header = Th08.Header(self._io, self, self._root)

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
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x54\x38\x52\x50":
                raise kaitaistruct.ValidationNotEqualError(b"\x54\x38\x52\x50", self.magic, self._io, u"/types/file_header/seq/0")
            self.version = self._io.read_bytes(2)
            self.unknown = self._io.read_bytes(6)
            self.userdata_offset = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.key = self._io.read_u1()
            self.unknown_3 = self._io.read_bytes(3)
            self.comp_size = self._io.read_u4le()
            self.decomp_size = self._io.read_u4le()
            self.stage_offsets = []
            for i in range(9):
                self.stage_offsets.append(self._io.read_u4le())

            self.potential_stage_size = []
            for i in range(9):
                self.potential_stage_size.append(self._io.read_u4le())



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
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(10), 0, False)).decode(u"ASCII")
            self.spell_card_id = self._io.read_u2le()
            self.spell_card_name = (KaitaiStream.bytes_terminate(self._io.read_bytes(50), 0, False)).decode(u"SJIS")
            self.score = self._io.read_u4le()
            self.unknown_4 = []
            for i in range(25):
                self.unknown_4.append(self._io.read_u4le())

            self.slowdown = self._io.read_f4le()


    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.score = self._io.read_u4le()
            self.point_items = self._io.read_u4le()
            self.graze = self._io.read_u4le()
            self.time = self._io.read_u4le()
            self.unknown = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.unknown_1 = self._io.read_u4le()
            self.power = self._io.read_u1()
            self.lives = self._io.read_u1()
            self.bombs = self._io.read_u1()
            self.unknown_2 = self._io.read_u1()


    @property
    def stages(self):
        if hasattr(self, '_m_stages'):
            return self._m_stages

        _pos = self._io.pos()
        self._m_stages = []
        for i in range(9):
            _on = self.file_header.stage_offsets[i]
            if _on == 0:
                self._m_stages.append(Th08.Dummy(self._io, self, self._root))
            else:
                self._io.seek(self.file_header.stage_offsets[i])
                self._m_stages.append(Th08.Stage(self._io, self, self._root))

        self._io.seek(_pos)
        return getattr(self, '_m_stages', None)


