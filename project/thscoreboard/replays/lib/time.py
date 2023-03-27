"""Functions to deal with time."""

import datetime


def strptime(date_string: str, format: str) -> datetime.datetime:
    """Returns a datetime created from a string input.

    Unlike datetime.datetime.strptime, this always returns a UTC datetime.
    """

    return datetime.datetime.strptime(date_string, format).replace(
        tzinfo=datetime.timezone.utc
    )
