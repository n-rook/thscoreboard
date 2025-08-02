# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class ThModern20Header(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.main = ThModern20Header.Main(self._io, self, self._root)
        self.userdata = ThModern20Header.Userdata(self._io, self, self._root)

    class Main(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic_ver = self._io.read_u4le()
            self.version = self._io.read_u4le()
            self.unused_1 = self._io.read_u4le()
            self.userdata_offset = self._io.read_u4le()
            self.unused_2 = self._io.read_bytes(24)
            self.comp_size = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.comp_data = self._io.read_bytes(self.comp_size)


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
            self.user_ver = ThModern20Header.Crlfstring(self._io, self, self._root)
            self.name = ThModern20Header.UserdataField(self._io, self, self._root)
            self.date = ThModern20Header.UserdataField(self._io, self, self._root)
            self.shot = ThModern20Header.UserdataField(self._io, self, self._root)
            self.difficulty = ThModern20Header.UserdataField(self._io, self, self._root)
            self.stage = ThModern20Header.Crlfstring(self._io, self, self._root)
            self.score = ThModern20Header.UserdataField(self._io, self, self._root)
            self.slowdown = ThModern20Header.UserdataField(self._io, self, self._root)


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
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes_term(32, False, True, True)).decode(u"ASCII")
            self.value = (self._io.read_bytes_term(13, False, True, True)).decode(u"ASCII")
            self.term = self._io.read_u1()



