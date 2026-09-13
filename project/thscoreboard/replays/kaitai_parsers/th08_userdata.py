# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th08Userdata(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Th08Userdata, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        if not self.magic == b"\x54\x38\x52\x50":
            raise kaitaistruct.ValidationNotEqualError(b"\x54\x38\x52\x50", self.magic, self._io, u"/seq/0")
        self.version = self._io.read_bytes(2)
        self.unknown = self._io.read_bytes(6)
        self.userdata_offset = self._io.read_u4le()


    def _fetch_instances(self):
        pass
        _ = self.userdata
        if hasattr(self, '_m_userdata'):
            pass
            self._m_userdata._fetch_instances()


    class Crlfstring(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th08Userdata.Crlfstring, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.value = (self._io.read_bytes_term(13, False, True, True)).decode(u"Shift_JIS")
            self.term = self._io.read_u1()


        def _fetch_instances(self):
            pass


    class Userdata(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th08Userdata.Userdata, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic_user = self._io.read_bytes(4)
            if not self.magic_user == b"\x55\x53\x45\x52":
                raise kaitaistruct.ValidationNotEqualError(b"\x55\x53\x45\x52", self.magic_user, self._io, u"/types/userdata/seq/0")
            self.user_length = self._io.read_u4le()
            self.unknown = self._io.read_bytes(4)
            self.name = Th08Userdata.UserdataField(self._io, self, self._root)
            self.date = Th08Userdata.UserdataField(self._io, self, self._root)
            self.shot = Th08Userdata.UserdataField(self._io, self, self._root)
            self.score = Th08Userdata.UserdataField(self._io, self, self._root)
            self.difficulty = Th08Userdata.UserdataField(self._io, self, self._root)
            self.cleared = Th08Userdata.UserdataField(self._io, self, self._root)
            self.mistakes = Th08Userdata.UserdataField(self._io, self, self._root)
            self.bombs = Th08Userdata.UserdataField(self._io, self, self._root)
            self.slowdown = Th08Userdata.UserdataField(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            self.name._fetch_instances()
            self.date._fetch_instances()
            self.shot._fetch_instances()
            self.score._fetch_instances()
            self.difficulty._fetch_instances()
            self.cleared._fetch_instances()
            self.mistakes._fetch_instances()
            self.bombs._fetch_instances()
            self.slowdown._fetch_instances()


    class UserdataField(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th08Userdata.UserdataField, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes_term(9, False, True, True)).decode(u"Shift_JIS")
            self.value = (self._io.read_bytes_term(13, False, True, True)).decode(u"Shift_JIS")
            self.term = self._io.read_u1()


        def _fetch_instances(self):
            pass


    @property
    def userdata(self):
        if hasattr(self, '_m_userdata'):
            return self._m_userdata

        _pos = self._io.pos()
        self._io.seek(self.userdata_offset)
        self._m_userdata = Th08Userdata.Userdata(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_userdata', None)


