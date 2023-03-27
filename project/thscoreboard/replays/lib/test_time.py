import datetime
import unittest

from replays.lib import time


class TimeTest(unittest.TestCase):
    def testStrptime(self):
        parsed_time = time.strptime("11/24/2001", "%m/%d/%Y")
        self.assertEqual(
            parsed_time, datetime.datetime(2001, 11, 24, tzinfo=datetime.timezone.utc)
        )
