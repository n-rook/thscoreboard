# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th08(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Th08, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.file_header = Th08.FileHeader(self._io, self, self._root)
        self.header = Th08.Header(self._io, self, self._root)


    def _fetch_instances(self):
        pass
        self.file_header._fetch_instances()
        self.header._fetch_instances()

    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th08.FileHeader, self).__init__(_io)
            self._parent = _parent
            self._root = _root
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
                self.stage_offsets.append(Th08.StagePointer(self._io, self, self._root))

            self.potential_stage_size = []
            for i in range(9):
                self.potential_stage_size.append(self._io.read_u4le())



        def _fetch_instances(self):
            pass
            for i in range(len(self.stage_offsets)):
                pass
                self.stage_offsets[i]._fetch_instances()

            for i in range(len(self.potential_stage_size)):
                pass



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th08.Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.unknown_1 = self._io.read_bytes(2)
            self.shot = self._io.read_u1()
            self.difficulty = self._io.read_u1()
            self.date = (KaitaiStream.bytes_terminate(self._io.read_bytes(6), 0, False)).decode(u"ASCII")
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(10), 0, False)).decode(u"Shift_JIS")
            self.spell_card_id = self._io.read_u2le()
            self.spell_card_name = (KaitaiStream.bytes_terminate(self._io.read_bytes(50), 0, False)).decode(u"Shift_JIS")
            self.score = self._io.read_u4le()
            self.unknown_4 = []
            for i in range(25):
                self.unknown_4.append(self._io.read_u4le())

            self.slowdown = self._io.read_f4le()


        def _fetch_instances(self):
            pass
            for i in range(len(self.unknown_4)):
                pass



    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th08.Stage, self).__init__(_io)
            self._parent = _parent
            self._root = _root
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


        def _fetch_instances(self):
            pass


    class StagePointer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th08.StagePointer, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()


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

            if self.offset != 0:
                pass
                _pos = self._io.pos()
                self._io.seek(self.offset)
                self._m_body = Th08.Stage(self._io, self, self._root)
                self._io.seek(_pos)

            return getattr(self, '_m_body', None)



