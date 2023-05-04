from datetime import datetime, timezone
from pathlib import Path
import unittest

from replays.management.commands.import_royalflare import (
    import_royalflare,
    parse_timestamp_from_json,
    parse_replay_path_from_json,
)
from replays.testing import test_case, test_replays
from replays import models


class ParseTimestampTest(unittest.TestCase):
    def testParseDateOnly(self):
        raw_timestamp = "2022/01/02"
        actual_timestamp = parse_timestamp_from_json(raw_timestamp)
        expected_timestamp = datetime(year=2022, month=1, day=2, tzinfo=timezone.utc)
        self.assertEqual(actual_timestamp, expected_timestamp)

    def testParseFullTimestamp(self):
        raw_timestamp = "2022/01/02 09:12:34"
        actual_timestamp = parse_timestamp_from_json(raw_timestamp)
        expected_timestamp = datetime(
            year=2022, month=1, day=2, hour=9, minute=12, second=34, tzinfo=timezone.utc
        )
        self.assertEqual(actual_timestamp, expected_timestamp)


class ParseReplayPathTest(unittest.TestCase):
    def testParseReplay(self):
        replay_directory = Path("some/directory/replays")
        raw_replay_location = "/replays/royalflare/th10/th10_ud1b3b.rpy"
        actual_path = parse_replay_path_from_json(replay_directory, raw_replay_location)
        expected_path = Path("some/directory/replays/royalflare/th10/th10_ud1b3b.rpy")
        self.assertEqual(actual_path, expected_path)


class ImportRoyalflareTest(test_case.ReplayTestCase):
    def testImportRoyalflareTh10(self):
        test_info_from_json = {
            "score": 294127890,
            "slowdown": "0.0%",
            "chara": "ReimuB",
            "difficulty": "Normal",
            "date": "2018/02/19 09:44",
            "player": "Test Player",
            "comment": "Test Comment",
            "replay": str(test_replays.TEST_REPLAY_LOCATION / "th10_normal.rpy"),
            "uploaded": "2022/01/01",
        }

        import_royalflare(test_info_from_json, test_replays.TEST_REPLAY_LOCATION.parent)

        imported_replay: models.Replay = models.Replay.objects.get()

        self.assertEqual(imported_replay.comment, "Test Comment")
        self.assertIsNone(imported_replay.user)
        self.assertEqual(imported_replay.imported_username, "Test Player")
        self.assertEqual(imported_replay.category, 1)
        self.assertEqual(
            imported_replay.created,
            datetime(
                year=2022,
                month=1,
                day=1,
                hour=0,
                minute=0,
                tzinfo=timezone.utc,
            ),
        )
        self.assertIsNone(imported_replay.route)
        self.assertTrue(imported_replay.is_good)
        self.assertTrue(imported_replay.is_clear)

    def testImportRoyalflareWithRoute(self):
        test_info_from_json = {
            "score": 3162240750,
            "slowdown": "0.00%",
            "chara": "Border Team",
            "difficulty": "Lunatic",
            "route": "FinalB",
            "date": "2022/01/03 13:02:30",
            "player": "Test Player",
            "comment": "Test Comment",
            "replay": str(test_replays.TEST_REPLAY_LOCATION / "th8_normal.rpy"),
            "uploaded": "2022/01/03",
        }

        import_royalflare(test_info_from_json, test_replays.TEST_REPLAY_LOCATION.parent)

        imported_replay: models.Replay = models.Replay.objects.get()
        self.assertEqual(imported_replay.route.GetName(), "Final B")
