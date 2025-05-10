import datetime
import unittest

from django import test

from replays.lib import time


class TimeTest(unittest.TestCase):
    def test_strptime(self):
        parsed_time = time.strptime("11/24/2001", "%m/%d/%Y")
        self.assertEqual(
            parsed_time, datetime.datetime(2001, 11, 24, tzinfo=datetime.timezone.utc)
        )

    def test_format_date_ja(self):
        self.enterContext(test.override_settings(LANGUAGE_CODE="ja"))
        self.assertEqual(
            time.format_date(datetime.datetime(year=2024, month=5, day=4)),
            "2024年 5月 4日",
        )

    def test_format_date_en(self):
        self.enterContext(test.override_settings(LANGUAGE_CODE="en"))
        self.assertEqual(
            time.format_date(datetime.datetime(year=2024, month=5, day=4)),
            "04 May 2024",
        )

    def test_format_month_day_ja(self):
        self.enterContext(test.override_settings(LANGUAGE_CODE="ja"))
        self.assertEqual(
            time.format_month_day(datetime.datetime(year=2024, month=5, day=4)), "5月 4日"
        )

    def test_format_month_day_en(self):
        self.enterContext(test.override_settings(LANGUAGE_CODE="en"))
        self.assertEqual(
            time.format_month_day(datetime.datetime(year=2024, month=5, day=4)),
            "04 May",
        )
