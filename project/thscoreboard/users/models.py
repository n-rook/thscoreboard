"""Defines models for the users app, which contains account information."""

import datetime
from typing import Optional
import secrets

from django.contrib.auth import base_user
from django.contrib.auth import models as auth_models
from django.contrib.auth import hashers
from django.contrib.auth import validators as auth_validators
from django.db import models
from django.db import transaction
from django.utils import timezone

from shared_content import model_ttl
from thscoreboard import settings


class User(auth_models.AbstractUser):
    """A user."""

    @classmethod
    def normalize_email(cls, email: str) -> str:
        """Provide access to normalize_email in a sensible place."""
        return base_user.BaseUserManager.normalize_email(email)

    class Meta(auth_models.AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint('email', name='unique_email')
        ]


_USERNAME_MAX_LENGTH = 150


class InvitedUser(models.Model):
    """A user who has been invited to join the site."""

    username = models.CharField(
        max_length=_USERNAME_MAX_LENGTH,
        validators=[auth_validators.UnicodeUsernameValidator()],
    )

    token = models.CharField(max_length=100, unique=True)
    """The secret email token used to verify ownership of the email address.

    We only expose this token in email messages, so if the user knows it, we
    know the address is theirs.
    """

    email = models.EmailField()

    created = models.DateTimeField(default=timezone.now)

    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    """The user who invited this person."""

    TTL = datetime.timedelta(days=365)

    @classmethod
    def CleanUp(cls, now: datetime.datetime) -> None:
        """Delete old invites.

        Args:
            now: The current time.

        Returns:
            The number of deleted invites.
        """
        model_ttl.CleanUpOldRows(cls, now)

    @classmethod
    def CreateInvite(cls, username, email, inviter):
        """Create a new invite.

        Be aware that this method does not check uniqueness for username and
        email. To be nice to the user, do this yourself.

        Args:
            username: The username for the new invitation.
            email: The email for the new invitation.
            inviter: The person inviting the new user.
        """

        if (inviter is None):
            raise ValueError('inviter cannot be None')

        normalized_email = User.normalize_email(email)
        token = secrets.token_urlsafe()

        invite = cls(
            username=username,
            email=normalized_email,
            invited_by=inviter,
            token=token)
        invite.save()
        return invite

    @transaction.atomic
    def AcceptInvite(self, password) -> 'User':
        """Convert an invite into a real, verified user.

        This method also deletes all of the "losers": any UnverifiedUser
        entries with the same username or email address. To the user,
        it will appear that their token became invalid.

        Returns:
            The new user.
        """
        u = User(
            username=User.normalize_username(self.username),
            email=User.normalize_email(self.email))
        u.set_password(password)
        u.save()

        self.delete()
        return u


class UnverifiedUser(models.Model):
    """A user who has not yet verified their email.

    Unverified users cannot log in.
    """

    username = models.CharField(
        max_length=_USERNAME_MAX_LENGTH,
        validators=[auth_validators.UnicodeUsernameValidator()],
    )

    password = models.CharField(max_length=200)
    """The hashed password."""

    token = models.CharField(max_length=100, unique=True)
    """The secret email token used to verify ownership of the email address.

    We only expose this token in email messages, so if the user knows it, we
    know the address is theirs.
    """

    email = models.EmailField()

    created = models.DateTimeField(default=timezone.now)

    TTL = datetime.timedelta(days=30)

    @classmethod
    def CleanUp(cls, now: datetime.datetime) -> None:
        """Delete old unverified users.

        Args:
            now: The current time.

        Returns:
            The number of deleted unverified users.
        """
        model_ttl.CleanUpOldRows(cls, now)

    def SetPassword(self, raw_password: str):
        """Hashes and sets the password. Identical to User.set_password()."""
        self.password = hashers.make_password(raw_password)

    def CheckPassword(self, raw_password: str) -> bool:
        """Return whether a user's password is correct.

        Similar to User.check_password.

        Args:
            raw_password: The raw, unencoded password from the user.

        Returns:
            True if the password matches, False otherwise.
        """
        return hashers.check_password(raw_password, self.password)

    @classmethod
    def CreateUser(cls, username, email, raw_password):
        """Create a new UnverifiedUser row.

        Be aware that this method does not check uniqueness for username and
        email. To be nice to the user, do this yourself.
        """
        normalized_email = User.normalize_email(email)
        password = hashers.make_password(raw_password)
        token = secrets.token_urlsafe()

        unverified_user = cls(
            username=username,
            password=password,
            email=normalized_email,
            token=token)
        unverified_user.save()
        return unverified_user

    @transaction.atomic
    def VerifyUser(self) -> 'User':
        """Convert an UnverifiedUser into a real, verified user.

        This method also deletes all of the "losers": any UnverifiedUser
        entries with the same username or email address. To the user,
        it will appear that their token became invalid.

        Returns:
            The new user.
        """
        u = User(
            username=User.normalize_username(self.username),
            email=User.normalize_email(self.email),
            password=self.password)
        u.save()
        # Delete all unverified users matching the new user's username or email.
        # After all, those tokens will no longer work.
        # Of course, that deletes this instance itself, too!
        type(self).objects.filter(models.Q(username=u.username) | models.Q(email=u.email)).delete()
        return u


class EarlyAccessPasscode(models.Model):

    passcode = models.TextField()
    """A passcode the user can supply to create an account."""


class UserPasscodeTie(models.Model):
    """Ties a user or an unverified user to a passcode."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    unverified_user = models.ForeignKey(UnverifiedUser, null=True, on_delete=models.CASCADE)
    passcode = models.ForeignKey('users.EarlyAccessPasscode', on_delete=models.CASCADE)


class Visits(models.Model):
    """Records the IP addresses of users visiting the website.

    This table exists to help identify users by IP if necessary.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)
    """The user who visited the website. If null, no one was logged in.

    Note that on_delete is PROTECT! Right now, it is not possible to delete a
    user from the site anyway. Of course, we will add this functionality at
    some point, but when we do it will be delayed; the user will request their
    account be deleted, we will mark it as "deleted" but keep it in the
    database, and then at some later point we will actually delete it from
    the database.
    """

    ip = models.TextField()
    """The IP address the user used to visit the site."""

    created = models.DateTimeField(default=timezone.now)
    """The time at which the user visited the site."""

    TTL = datetime.timedelta(days=41)

    @classmethod
    def _WasThereARecentVisit(cls, user: Optional[settings.AUTH_USER_MODEL], ip: str, threshold: datetime.datetime):
        return cls.objects.filter(user=user, ip=ip, created__gt=threshold)

    @classmethod
    def RecordVisit(cls, user: Optional[settings.AUTH_USER_MODEL], ip: str):
        """Record a visit to this site.

        Visits are only recorded at most once every hour.
        """
        now = timezone.now()
        an_hour_ago = now - datetime.timedelta(hours=1)

        with transaction.atomic():
            if cls._WasThereARecentVisit(user, ip, an_hour_ago):
                return

            new_visit = cls(user=user, ip=ip, created=now)
            new_visit.save()
