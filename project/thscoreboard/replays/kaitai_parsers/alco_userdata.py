# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class AlcoUserdata(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.main = AlcoUserdata.Main(self._io, self, self._root)
        self.userdata = AlcoUserdata.Userdata(self._io, self, self._root)

    class Main(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic_ver = self._io.read_bytes(4)
            if not self.magic_ver == b"\x61\x6C\x31\x72":
                raise kaitaistruct.ValidationNotEqualError(b"\x61\x6C\x31\x72", self.magic_ver, self._io, u"/types/main/seq/0")
            self.version = self._io.read_u4le()
            self.unused_1 = self._io.read_u4le()
            self.userdata_offset = self._io.read_u4le()
            self.unused_2 = self._io.read_bytes(12)
            self.len_comp_data = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.comp_data = self._io.read_bytes(self.len_comp_data)


    class Userdata(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic_user = self._io.read_bytes(4)
            if not self.magic_user == b"\x55\x53\x45\x52":
                raise kaitaistruct.ValidationNotEqualError(b"\x55\x53\x45\x52", self.magic_user, self._io, u"/types/userdata/seq/0")
            self.user_length = self._io.read_u4le()
            self.unknown = self._io.read_bytes(4)
            self.user_desc = []
            i = 0
            while True:
                _ = self._io.read_u1()
                self.user_desc.append(_)
                if _ == 13:
                    break
                i += 1
            self.user_desc_term = (self._io.read_bytes_term(10, False, True, True)).decode(u"ASCII")
            self.user_ver = AlcoUserdata.UserdataField(u"Version", self._io, self, self._root)
            self.name = AlcoUserdata.UserdataField(u"Name", self._io, self, self._root)
            self.date = AlcoUserdata.UserdataField(u"Date", self._io, self, self._root)
            self.stage = AlcoUserdata.UserdataField(u"Stage", self._io, self, self._root)
            self.score = AlcoUserdata.UserdataField(u"Score", self._io, self, self._root)
            self.slowdown = AlcoUserdata.UserdataField(u"Slow Rate", self._io, self, self._root)


    class Crlfstring(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.value = (self._io.read_bytes_term(13, False, True, True)).decode(u"SJIS")
            self.term = self._io.read_u1()


    class UserdataField(KaitaiStruct):
        def __init__(self, expected_name, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.expected_name = expected_name
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes(len(self.expected_name))).decode(u"ASCII")
            if not self.name == self.expected_name:
                raise kaitaistruct.ValidationNotEqualError(self.expected_name, self.name, self._io, u"/types/userdata_field/seq/0")
            self.name_value_separator_space = self._io.read_bytes(1)
            if not self.name_value_separator_space == b"\x20":
                raise kaitaistruct.ValidationNotEqualError(b"\x20", self.name_value_separator_space, self._io, u"/types/userdata_field/seq/1")
            self.value_with_space = (self._io.read_bytes_term(10, False, True, True)).decode(u"ASCII")

        @property
        def value(self):
            if hasattr(self, '_m_value'):
                return self._m_value

            self._m_value = (self.value_with_space)[0:(len(self.value_with_space) - 1)]
            return getattr(self, '_m_value', None)



