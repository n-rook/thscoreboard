import unittest

from replays.testing import test_replays
from replays import replay_parsing
from replays.game_ids import GameIDs
from replays.replay_parsing import ReplayInfo
from replays.game_fields import GetFormatPower, GetFormatStage


def ParseTestReplay(filename: str) -> ReplayInfo:
    return replay_parsing.Parse(test_replays.GetRaw(filename))


class FormatStageTestCase(unittest.TestCase):
    def testNoneStage(self) -> None:
        format_stage = GetFormatStage(GameIDs.TH06, None)
        self.assertEqual(format_stage, "")

    def testTh07(self) -> None:
        format_stage_2 = GetFormatStage(GameIDs.TH07, 2)
        self.assertEqual(format_stage_2, "2")
        format_stage_ex = GetFormatStage(GameIDs.TH07, 7)
        self.assertEqual(format_stage_ex, "Extra")
        format_stage_ex = GetFormatStage(GameIDs.TH07, 8)
        self.assertEqual(format_stage_ex, "Phantasm")

    def testTh08(self) -> None:
        format_stage_2 = GetFormatStage(GameIDs.TH08, 2)
        self.assertEqual(format_stage_2, "2")
        format_stage_4A = GetFormatStage(GameIDs.TH08, 4)
        self.assertEqual(format_stage_4A, "4A")
        format_stage_6B = GetFormatStage(GameIDs.TH08, 8)
        self.assertEqual(format_stage_6B, "6B")
        format_stage_ex = GetFormatStage(GameIDs.TH08, 9)
        self.assertEqual(format_stage_ex, "Extra")

    def testTh09(self) -> None:
        format_stage_2 = GetFormatStage(GameIDs.TH09, 2)
        self.assertEqual(format_stage_2, "2")
        format_stage_7 = GetFormatStage(GameIDs.TH09, 7)
        self.assertEqual(format_stage_7, "7")
        format_stage_ex = GetFormatStage(GameIDs.TH09, 10)
        self.assertEqual(format_stage_ex, "Extra")

    def testDefault(self) -> None:
        format_stage_2 = GetFormatStage(GameIDs.TH06, 2)
        self.assertEqual(format_stage_2, "2")
        format_stage_6 = GetFormatStage(GameIDs.TH06, 6)
        self.assertEqual(format_stage_6, "6")
        format_stage_ex = GetFormatStage(GameIDs.TH06, 7)
        self.assertEqual(format_stage_ex, "Extra")

        format_stage_2 = GetFormatStage(GameIDs.TH10, 2)
        self.assertEqual(format_stage_2, "2")


class FormatPowerTestCase(unittest.TestCase):
    def testNonePower(self) -> None:
        format_power = GetFormatPower(GameIDs.TH06, None)
        self.assertEqual(format_power, "")

    def testTh07(self) -> None:
        format_power = GetFormatPower(GameIDs.TH07, 49)
        self.assertEqual(format_power, "49")

    def testTh11(self) -> None:
        format_20_power = GetFormatPower(GameIDs.TH11, 20, "ReimuA")
        self.assertEqual(format_20_power, "1.00")
        format_49_power = GetFormatPower(GameIDs.TH11, 49, "ReimuA")
        self.assertEqual(format_49_power, "2.45")

        format_0_power_marisa_a = GetFormatPower(GameIDs.TH11, 0, "MarisaA")
        self.assertEqual(format_0_power_marisa_a, "0.00")
        format_49_power_marisa_a = GetFormatPower(GameIDs.TH11, 49, "MarisaA")
        self.assertEqual(format_49_power_marisa_a, "4.08")
        format_8_power_marisa_a = GetFormatPower(GameIDs.TH11, 8, "MarisaA")
        self.assertEqual(format_8_power_marisa_a, "0.67")

    def testTh12(self) -> None:
        format_100_power = GetFormatPower(GameIDs.TH12, 100)
        self.assertEqual(format_100_power, "1.00")
        format_49_power = GetFormatPower(GameIDs.TH12, 49)
        self.assertEqual(format_49_power, "0.49")
