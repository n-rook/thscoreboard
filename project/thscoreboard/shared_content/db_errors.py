from django.db import utils
from psycopg2 import errors


def IsUniqueError(e: utils.IntegrityError) -> bool:
    """Return whether the error was caused by a unique constraint."""

    return isinstance(e.__cause__, errors.UniqueViolation)


def GetUniqueConstraintCause(e: utils.IntegrityError) -> str:
    """Returns the unique constraint that caused an error."""

    if not IsUniqueError(e):
        raise ValueError("The exception passed was not a unique constraint error.")

    unique_violation: errors.UniqueViolation = e.__cause__
    constraint_name = unique_violation.diag.constraint_name
    if not constraint_name:
        raise ValueError(
            f"Unexpected error: Exception {unique_violation} had no constraint_name"
        )

    return constraint_name
