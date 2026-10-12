# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Th20(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Th20, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.header = Th20.Header(self._io, self, self._root)
        self.stages = []
        for i in range(self.header.stage_count):
            self.stages.append(Th20.Stage(self._io, self, self._root))



    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        for i in range(len(self.stages)):
            pass
            self.stages[i]._fetch_instances()


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th20.Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(16), 0, False)).decode(u"Shift_JIS")
            self.timestamp = self._io.read_u8le()
            self.score = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(180)
            self.slowdown = self._io.read_f4le()
            self.stage_count = self._io.read_u4le()
            self.shot = self._io.read_u4le()
            self.stones = []
            for i in range(4):
                self.stones.append(self._io.read_u4le())

            self.unknown_2 = self._io.read_bytes(4)
            self.difficulty = self._io.read_u4le()
            self.unknown_3 = self._io.read_bytes(4)
            self.unknown_4 = self._io.read_bytes(4)
            self.spell_practice_id = self._io.read_u4le()


        def _fetch_instances(self):
            pass
            for i in range(len(self.stones)):
                pass



    class Stage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Th20.Stage, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.stage_num = self._io.read_u4le()
            self.rng = self._io.read_u4le()
            self.frame_count = self._io.read_u4le()
            self.len_stage_data = self._io.read_u4le()
            self.pos_subpixel_x = self._io.read_u4le()
            self.pos_subpixel_y = self._io.read_u4le()
            self.unknown_1 = self._io.read_bytes(88)
            self.score = self._io.read_u4le()
            self.unknown_2 = self._io.read_bytes(44)
            self.power = self._io.read_u4le()
            self.power_max = self._io.read_u4le()
            self.unknown_3 = self._io.read_bytes(4)
            self.graze = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()
            self.piv = self._io.read_u4le()
            self.unknown_5 = self._io.read_u4le()
            self.anomaly_attack_gauge = self._io.read_u4le()
            self.unknown_6 = self._io.read_bytes(20)
            self.unknown_7 = self._io.read_bytes(16)
            self.stones_levels = []
            for i in range(4):
                self.stones_levels.append(self._io.read_u4le())

            self.anomaly_levels = []
            for i in range(4):
                self.anomaly_levels.append(self._io.read_u4le())

            self.total_stone_level = self._io.read_u4le()
            self.unknown_8 = self._io.read_bytes(32)
            self.lives = self._io.read_u4le()
            self.lives_max = self._io.read_u4le()
            self.life_pieces = self._io.read_u4le()
            self.unknown_9 = self._io.read_bytes(4)
            self.unknown_10 = self._io.read_bytes(4)
            self.bombs = self._io.read_u4le()
            self.bomb_pieces = self._io.read_u4le()
            self.unknown_11 = self._io.read_bytes(4)
            self.bombs_max = self._io.read_u4le()
            self.unknown_12 = self._io.read_bytes(332)
            self.unknown_13 = self._io.read_f4le()
            self.unknown_14 = self._io.read_f4le()
            self.stage_data = self._io.read_bytes(self.len_stage_data)


        def _fetch_instances(self):
            pass
            for i in range(len(self.stones_levels)):
                pass

            for i in range(len(self.anomaly_levels)):
                pass




