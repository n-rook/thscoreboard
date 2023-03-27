"""Helps implement rows with TTLs."""

import datetime
import logging
import typing

from django.db import models


class TTLModelType(typing.Protocol):
    """A type hint class specifying a model type with a TTL.

    Objects older than the TTL (checking by their "created" field) will be
    deleted by CleanUpOldRows.

    CleanUpOldRows only accepts models with a "TTL" field specifying the TTL
    and a "created" row specifying the time a row was created. Unfortunately,
    this kind of weird class is the best way I can find to specify that
    requirement in Python's type system.
    """

    @property
    def TTL(self) -> datetime.timedelta:
        pass

    @property
    def created(self) -> models.DateTimeField:
        pass

    @property
    def __name__(self) -> str:
        pass


def CleanUpOldRows(model_class: TTLModelType, now: datetime.datetime):
    """Clean up old rows in a table.

    Args:
        model_class: The table for which to clean up old rows.
    """
    earliest_surviving_time = now - model_class.TTL

    logging.info(
        "Deleting all %s rows before %s",
        model_class.__name__,
        earliest_surviving_time,
    )

    deleted_count, _ = model_class.objects.filter(
        created__lt=earliest_surviving_time
    ).delete()
    logging.info("Deleted %d %s rows", deleted_count, model_class.__name__)
