# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th125Encrypted(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Th125Encrypted.FileHeader(self._io, self, self._root)

    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x74\x31\x32\x35":
                raise kaitaistruct.ValidationNotEqualError(b"\x74\x31\x32\x35", self.magic, self._io, u"/types/file_header/seq/0")
            self.unknown_1 = self._io.read_bytes(8)
            self.userdata_offset = self._io.read_u4le()


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
            self.version = Th125Encrypted.UserdataField(u"Version", self._io, self, self._root)
            self.username = Th125Encrypted.UserdataField(u"Name", self._io, self, self._root)
            self.date = Th125Encrypted.UserdataField(u"Date", self._io, self, self._root)
            self.shot = Th125Encrypted.UserdataField(u"Chara", self._io, self, self._root)
            self.level_scene = Th125Encrypted.LevelSceneField(self._io, self, self._root)
            self.score = Th125Encrypted.UserdataField(u"Score", self._io, self, self._root)
            self.slowdown = Th125Encrypted.UserdataField(u"Slow Rate", self._io, self, self._root)


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


    class LevelSceneField(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.level = (self._io.read_bytes_term(45, False, True, True)).decode(u"ASCII")
            self.scene = (self._io.read_bytes_term(13, False, True, True)).decode(u"ASCII")
            self.lf = self._io.read_bytes(1)
            if not self.lf == b"\x0A":
                raise kaitaistruct.ValidationNotEqualError(b"\x0A", self.lf, self._io, u"/types/level_scene_field/seq/2")


    @property
    def userdata(self):
        if hasattr(self, '_m_userdata'):
            return self._m_userdata

        _pos = self._io.pos()
        self._io.seek(self.header.userdata_offset)
        self._m_userdata = Th125Encrypted.Userdata(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_userdata', None)


