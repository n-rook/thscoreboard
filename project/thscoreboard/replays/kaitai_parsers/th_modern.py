# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class ThModern(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(ThModern, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.main = ThModern.Main(self._io, self, self._root)
        self.userdata = ThModern.Userdata(self._io, self, self._root)


    def _fetch_instances(self):
        pass
        self.main._fetch_instances()
        self.userdata._fetch_instances()

    class Crlfstring(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(ThModern.Crlfstring, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.value = (self._io.read_bytes_term(13, False, True, True)).decode(u"Shift_JIS")
            self.term = self._io.read_u1()


        def _fetch_instances(self):
            pass


    class Main(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(ThModern.Main, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic_ver = self._io.read_u4le()
            self.version = self._io.read_u4le()
            self.unused_1 = self._io.read_u4le()
            self.userdata_offset = self._io.read_u4le()
            self.unused_2 = self._io.read_bytes(12)
            self.len_comp_data = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.comp_data = self._io.read_bytes(self.len_comp_data)


        def _fetch_instances(self):
            pass


    class Userdata(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(ThModern.Userdata, self).__init__(_io)
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
            self.user_ver = ThModern.Crlfstring(self._io, self, self._root)
            self.name = ThModern.UserdataField(self._io, self, self._root)
            self.date = ThModern.UserdataField(self._io, self, self._root)
            self.shot = ThModern.UserdataField(self._io, self, self._root)
            self.difficulty = ThModern.UserdataField(self._io, self, self._root)
            self.stage = ThModern.Crlfstring(self._io, self, self._root)
            self.score = ThModern.UserdataField(self._io, self, self._root)
            self.slowdown = ThModern.UserdataField(self._io, self, self._root)


        def _fetch_instances(self):
            pass
            for i in range(len(self.user_desc)):
                pass

            self.user_ver._fetch_instances()
            self.name._fetch_instances()
            self.date._fetch_instances()
            self.shot._fetch_instances()
            self.difficulty._fetch_instances()
            self.stage._fetch_instances()
            self.score._fetch_instances()
            self.slowdown._fetch_instances()


    class UserdataField(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(ThModern.UserdataField, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes_term(32, False, True, True)).decode(u"ASCII")
            self.value = (self._io.read_bytes_term(13, False, True, True)).decode(u"ASCII")
            self.term = self._io.read_u1()


        def _fetch_instances(self):
            pass



