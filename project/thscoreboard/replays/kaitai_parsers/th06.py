# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th06(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Th06.Header(self._io, self, self._root)

    class Dummy(KaitaiStruct):
        """blank type."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_2 = self._io.read_u1()
            self.date = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.unknown_3 = self._io.read_u2le()
            self.score = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()
            self.slowdown = self._io.read_f4le()
            self.unknown_5 = self._io.read_u4le()
            self.stage_offsets = []
            for i in range(7):
                self.stage_offsets.append(self._io.read_u4le())



    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.score = self._io.read_u4le()
            self.seed = self._io.read_u2le()
            self.unknown_1 = self._io.read_u2le()
            self.power = self._io.read_u1()
            self.lives = self._io.read_s1()
            self.bombs = self._io.read_s1()
            self.rank = self._io.read_u1()


    @property
    def stages(self):
        if hasattr(self, '_m_stages'):
            return self._m_stages

        _pos = self._io.pos()
        self._m_stages = []
        for i in range(7):
            _on = self.header.stage_offsets[i]
            if _on == 0:
                self._m_stages.append(Th06.Dummy(self._io, self, self._root))
            else:
                #   the th06 decryptor only returns the decrypted data instead of the full file
                #   the game stores these stage offsets from the start of the file
                #   thus we must adjust them to account for this difference when reading the stage data
                self._io.seek(self.header.stage_offsets[i]-15)
                self._m_stages.append(Th06.Stage(self._io, self, self._root))

        self._io.seek(_pos)
        return getattr(self, '_m_stages', None)


