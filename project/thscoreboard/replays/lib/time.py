"""Functions to deal with time."""

import datetime

from django.utils import formats
from django.utils import translation


def strptime(date_string: str, format: str) -> datetime.datetime:
    """Returns a datetime created from a string input.

    Unlike datetime.datetime.strptime, this always returns a UTC datetime.
    """

    return datetime.datetime.strptime(date_string, format).replace(
        tzinfo=datetime.timezone.utc
    )


def format_month_day(timestamp) -> str:
    if translation.get_language() == "ja":
        f = "n月 j日"
    else:  # en
        f = "d F"
    return formats.date_format(timestamp, format=f)


def format_date(timestamp) -> str:
    if translation.get_language() == "ja":
        f = "Y年 n月 j日"
    else:  # en
        f = "d F y"
    return formats.date_format(timestamp, format=f)
