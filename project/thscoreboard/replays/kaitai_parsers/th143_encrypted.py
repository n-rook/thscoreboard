# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th143Encrypted(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Th143Encrypted, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.header = Th143Encrypted.FileHeader(self._io, self, self._root)


    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        _ = self.userdata
        if hasattr(self, '_m_userdata'):
            pass
            self._m_userdata._fetch_instances()


    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th143Encrypted.FileHeader, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x74\x31\x34\x33":
                raise kaitaistruct.ValidationNotEqualError(b"\x74\x31\x34\x33", self.magic, self._io, u"/types/file_header/seq/0")
            self.unknown_1 = self._io.read_bytes(8)
            self.userdata_offset = self._io.read_u4le()


        def _fetch_instances(self):
            pass


    class Userdata(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th143Encrypted.Userdata, self).__init__(_io)
            self._parent = _parent
            self._root = _root
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
            self.version = Th143Encrypted.UserdataField(u"Version", self._io, self, self._root)
            self.username = Th143Encrypted.UserdataField(u"Name", self._io, self, self._root)
            self.date = Th143Encrypted.UserdataField(u"Date", self._io, self, self._root)
            self.level = Th143Encrypted.UserdataField(u"Day", self._io, self, self._root)
            self.scene = Th143Encrypted.UserdataField(u"Scene", self._io, self, self._root)
            self.score = Th143Encrypted.UserdataField(u"Score", self._io, self, self._root)
            self.slowdown = Th143Encrypted.UserdataField(u"Slow Rate", self._io, self, self._root)


        def _fetch_instances(self):
            pass
            for i in range(len(self.user_desc)):
                pass

            self.version._fetch_instances()
            self.username._fetch_instances()
            self.date._fetch_instances()
            self.level._fetch_instances()
            self.scene._fetch_instances()
            self.score._fetch_instances()
            self.slowdown._fetch_instances()


    class UserdataField(KaitaiStruct):
        def __init__(self, expected_name, _io, _parent=None, _root=None):
            super(Th143Encrypted.UserdataField, self).__init__(_io)
            self._parent = _parent
            self._root = _root
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


        def _fetch_instances(self):
            pass

        @property
        def value(self):
            if hasattr(self, '_m_value'):
                return self._m_value

            self._m_value = self.value_with_space[0:len(self.value_with_space) - 1]
            return getattr(self, '_m_value', None)


    @property
    def userdata(self):
        if hasattr(self, '_m_userdata'):
            return self._m_userdata

        _pos = self._io.pos()
        self._io.seek(self.header.userdata_offset)
        self._m_userdata = Th143Encrypted.Userdata(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_userdata', None)


