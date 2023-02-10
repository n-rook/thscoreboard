"""Defines models for the users app, which contains account information."""

import datetime
import logging
from typing import Optional
import secrets

from django.core.exceptions import ValidationError
from django.contrib.auth import models as auth_models
from django.contrib.auth import hashers
from django.contrib.auth import validators as auth_validators
from django.db import models
from django.db import transaction
from django.utils import timezone
from ipaddress import ip_network

from shared_content import model_ttl
from thscoreboard import settings


class BannedError(Exception):
    """Raised if an operation is impossible because a username or email is banned."""


class User(auth_models.AbstractUser):
    """A user."""

    _DELETED_ACCOUNT_TTL = datetime.timedelta(days=60)
    """The amount of time for which a deleted account persists."""

    @classmethod
    def normalize_email(cls, email: str) -> str:
        """Provide access to normalize_email in a sensible place."""
        return cls.objects.normalize_email(email)

    class Meta(auth_models.AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint('email', name='unique_email'),
            models.CheckConstraint(
                check=(
                    models.Q(deleted_on__isnull=False) & models.Q(is_active=False)
                ) | (
                    models.Q(deleted_on__isnull=True) & models.Q(is_active=True)
                ),
                name='deleted_on_set_iff_not_active'),
        ]

    deleted_on = models.DateTimeField(null=True, blank=True)
    """The time at which the user requested their account be deleted.

    In order to protect users whose accounts were hacked or who had second thoughts,
    we keep deleted accounts around for a while even after the user requests they
    be deleted.
    """

    might_be_banned = models.BooleanField(default=False)
    """A field that is false if the user is definitely not banned.

    If this field is True, the user might or might not be banned. As such,
    this is useful as a cache, so that an extra database call isn't necessary
    to find out if the user is banned or not, but it should not be taken as
    authoritative (unless its value is False).
    """

    @classmethod
    def CleanUp(cls, now: datetime.datetime):
        """Remove long-deleted accounts and other data."""

        earliest_surviving_time = now - User._DELETED_ACCOUNT_TTL
        logging.info('Deleting accounts marked for deletion before %s', earliest_surviving_time)

        count = 0
        for user in User.objects.filter(
            is_active=False,
            deleted_on__lte=earliest_surviving_time
        ):
            with transaction.atomic():
                Ban.PropagateAccountDeletion(user)
                user.delete()
            count += 1
        logging.info('Cleaned up %d accounts marked for deletion.', count)

    def CheckIfBanned(self) -> bool:
        """Check whether this user is banned or not.

        This method will not conduct a database call in most cases, but in
        some cases it will. Sometimes, it will even write to the database.
        """

        if not self.is_authenticated:
            return False

        if not self.might_be_banned:
            return False

        now = datetime.datetime.now(datetime.timezone.utc)
        if Ban.objects.filter(target=self, expiration__gt=now).exists():
            return True

        # The user is not really banned, but might_be_banned is true!
        # Better fix that.
        self.might_be_banned = False
        self.save()
        return False

    def BanUser(self, author: 'User', reason: str, duration: datetime.timedelta, expiration: Optional[datetime.datetime] = None) -> 'Ban':
        """Ban this user for a specified period of time.

        Note that this method calls save() on this instance.

        Args:
            author: The user doing the banning.
            reason: The reason why the user is going to be banned.
            duration: How long the ban should last.
            expiration: The time at which the ban should expire. Here mostly
                for testing; if not set, the expiration time is calculated from
                the current time and the duration specified.

        Returns:
            The Ban created.
        """

        if expiration is None:
            expiration = datetime.datetime.now(datetime.timezone.utc) + duration

        b = Ban.objects.create(
            author=author,
            target=self,
            reason=reason,
            duration=duration,
            expiration=expiration
        )
        self.might_be_banned = True
        self.save()
        return b

    @transaction.atomic
    def MarkForDeletion(self):
        """Mark this account for deletion."""
        self.is_active = False
        self.deleted_on = datetime.datetime.now(datetime.timezone.utc)
        self.save()


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

        Raises:
            BannedError: If the username or email are taken by a banned user. This should be
                very rare--- how did the UnverifiedUser get created in the first place if this
                is the case?--- but it is not impossible.
        """
        if Ban.IsUsernameBanned(self.username):
            raise BannedError(f'The username {self.username} is currently suspended.')
        if Ban.IsEmailBanned(self.email):
            raise BannedError(f'The address {self.email} is currently suspended.')

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
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    """The user who visited the website. If null, no one was logged in.

    on_delete is CASCADE, but the on_delete mode has no effect anyway: the time between a user marking
    their account for deletion and it actually being deleted is greater than the TTL of this table.
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
                return None

            new_visit = cls(user=user, ip=ip, created=now)
            new_visit.save()
            return new_visit

    @classmethod
    def CleanUp(cls, now: datetime.datetime) -> None:
        """Delete old visits.

        Args:
            now: The current time.

        Returns:
            The number of deleted visits.
        """
        model_ttl.CleanUpOldRows(cls, now)


def validate_ip(ip):
    try:
        ip_network(ip)
    except ValueError as e:
        raise ValidationError(e)


class IPBan(models.Model):
    """Keeps a list of IP subnets of IPs banned from signup"""

    ip = models.TextField(validators=[validate_ip])
    """The IP address banned from signups"""

    comment = models.TextField(null=True)
    """Optional reason for the ban"""

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    """Who issued the ban"""


class Ban(models.Model):
    """Records users who have been temporarily banned from the site.

    Bans are permanently recorded in this table. However, all bans are
    temporary; the time a ban expires is also recorded here.
    """

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(target__isnull=True) & models.Q(deleted_account_username__isnull=False) & models.Q(deleted_account_email__isnull=False)
                ) | (
                    models.Q(target__isnull=False) & models.Q(deleted_account_username__isnull=True) & models.Q(deleted_account_email__isnull=True)
                ),
                name='target_null_iff_deleted_account_fields_are_set'
            )
        ]

    indexes = [
        models.Index(
            ['target', 'expiration'],
            name='BanLookupByTargetAndExpiration'),
        models.Index(
            ['deleted_account_username', 'expiration'],
            name='BanLookupByDeletedAccountUsernameAndExpiration'
        ),
        models.Index(
            ['deleted_account_email', 'expiration'],
            name='BanLookupByDeletedAccountEmailAndExpiration'
        ),
    ]

    _DELETED_ACCOUNT_TTL = datetime.timedelta(days=30)
    """How long to keep bans from deleted accounts after the ban expires.

    This is 30 days so that if the person tries to reregister immediately, we have
    historical context on why they were banned in the first place.
    """

    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    """The user who was banned.

    This field is defined with a PROTECT on_delete policy. If you need to delete a user,
    first call PropagateAccountDeletion() to remove that user from target fields in the
    ban table.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_ban')
    """Who issued the ban."""

    reason = models.TextField(blank=True)
    """The reason the user was banned.

    This will be visible to the banned user.
    """

    expiration = models.DateTimeField()
    """The time at which the ban will expire."""

    duration = models.DurationField()
    """The duration of the ban.

    This field has no direct effect, but the duration of bans is recorded for posterity.
    """

    # These two fields are only set for users who delete their accounts while
    # they are banned. This way, banned users can delete their accounts and remove
    # all their content from the site, but cannot reregister under the same
    # name or email address.
    deleted_account_username = models.TextField(null=True, blank=True)
    """The username this ban's target had before they deleted their account."""

    deleted_account_email = models.EmailField(null=True, blank=True)
    """The email this ban's target had before they deleted their account."""

    @classmethod
    @transaction.atomic
    def PropagateAccountDeletion(cls, user_being_deleted: 'User'):
        """If a User row is about to be deleted, update their bans accordingly.

        This method makes the following changes:
        * The "target" field is set to null.
        * The "deleted_account_username" and "deleted_account_email" fields are set to the user's
        * current name and email.
        """
        for b in cls.objects.filter(target=user_being_deleted):
            b.deleted_account_username = user_being_deleted.username
            b.deleted_account_email = user_being_deleted.email
            b.target = None
            b.save()

    @classmethod
    def IsUsernameBanned(cls, username: str, now: Optional[datetime.datetime] = None) -> bool:
        """Returns whether a username is banned (as a deleted account).

        Note that this will return False if a user has an active, banned account with this username.
        """
        if not now:
            now = datetime.datetime.now(datetime.timezone.utc)
        return cls.objects.filter(deleted_account_username=username, expiration__gte=now).exists()

    @classmethod
    def IsEmailBanned(cls, email: str, now: Optional[datetime.datetime] = None) -> bool:
        """Returns whether an email address is banned (as a deleted account).

        Note that this will return False if a user has an active, banned account with this address.
        """
        if not now:
            now = datetime.datetime.now(datetime.timezone.utc)
        return cls.objects.filter(deleted_account_email=email, expiration__gte=now).exists()

    @classmethod
    def CleanUp(cls, now: datetime.datetime) -> None:
        """Delete long-expired bans from deleted accounts.

        Args:
            now: The current time.

        Returns:
            The number of deleted bans.
        """
        earliest_surviving_time = now - cls._DELETED_ACCOUNT_TTL
        logging.info('Deleting bans of deleted accounts which expired before %s',
                     earliest_surviving_time)

        count = 0
        for b in cls.objects.filter(
            target__isnull=True,
            expiration__lte=earliest_surviving_time
        ):
            with transaction.atomic():
                b.delete()
            count += 1

        logging.info('Cleaned up %d bans.', count)
