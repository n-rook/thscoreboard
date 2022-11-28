"""Parse a CSV file of username/password pairs."""

from __future__ import annotations

import csv
import dataclasses

from users import models


def Parse(csv_contents: str) -> list[InviteRow]:
    """Parse a CSV file.

    Args:
        csv_contents: The CSV file, as a string.

    Returns:
        A CSVInvites instance.
    """
    parsed_rows = []
    for row in csv.reader(csv_contents.split('\n')):
        if len(row) > 0:
            parsed_rows.append(_ToInviteRow(row))
    return parsed_rows


def _ToInviteRow(row):
    errors = []
    warnings = []

    if len(row) > 0:
        username = row[0]
    else:
        username = ''

    username = models.User.normalize_username(username)
    if not username:
        errors.append('No username')
    try:
        existing_user = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        pass
    else:
        errors.append(f'User already exists ({existing_user.email})')

    existing_invites = models.InvitedUser.objects.filter(username__exact=username)
    if existing_invites:
        warnings.append('User already invited ({})'.format(
            ', '.join([i.email for i in existing_invites])
        ))

    if len(row) > 1:
        email = row[1]
    else:
        email = ''

    email = models.User.normalize_email(email)
    if not email:
        errors.append('No email')
    try:
        existing_user = models.User.objects.get(email=email)
    except models.User.DoesNotExist:
        pass
    else:
        errors.append(f'User already exists ({existing_user.username})')

    existing_invites = models.InvitedUser.objects.filter(email__exact=email)
    if existing_invites:
        warnings.append('User already invited ({})'.format(
            ', '.join([i.username for i in existing_invites])
        ))

    if len(row) > 2:
        warnings.append('Extra content in row: ' + ','.join(row[2:]))

    return InviteRow(username, email, errors, warnings)


@dataclasses.dataclass(frozen=True)
class InviteRow:

    username: str
    """The username the invited user will get."""

    email: str
    """The email the invited user will get."""

    errors: list[str]
    """Errors that will prevent this user from being invited."""

    warnings: list[str]
    """Warnings that do not prevent invitation, but that you might want to check out."""

    @property
    def errors_str(self):
        return '; '.join(self.errors)

    @property
    def warnings_str(self):
        return '; '.join(self.warnings)

    def IsValid(self):
        return not bool(self.errors)
