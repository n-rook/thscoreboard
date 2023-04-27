import datetime
from typing import Any, Optional


from django import forms
from django.contrib import auth
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

from replays.models import Replay
from . import models


class UsernameField(forms.CharField):
    def to_python(self, value: Optional[Any]) -> Optional[str]:
        value = super().to_python(value)
        if value is None:
            return None

        return models.User.normalize_username(value)

    def validate(self, value):
        if value is None:
            return True

        if (
            models.User.objects.filter(username=value)
            or models.Ban.IsUsernameBanned(value)
            or models.InvitedUser.objects.filter(username=value)
        ):
            raise exceptions.ValidationError(
                _("An account has already been registered with this username.")
            )


class UserEmailField(forms.EmailField):
    def to_python(self, value: Optional[Any]) -> Optional[str]:
        value = super().to_python(value)
        if value is None:
            return None

        return models.User.normalize_email(value)

    def validate(self, value):
        if value is None:
            return True

        if (
            models.User.objects.filter(email=value)
            or models.Ban.IsEmailBanned(value)
            or models.InvitedUser.objects.filter(email=value)
        ):
            raise exceptions.ValidationError(
                _("An account has already been registered with this email address.")
            )


class RegisterForm(forms.Form):
    username = UsernameField(label="username", max_length=30)
    email = UserEmailField(label="email", max_length=200)
    password = forms.CharField(
        label="password", max_length=200, widget=forms.PasswordInput
    )


class DeleteAccountForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    password = forms.CharField(
        label="password", max_length=200, widget=forms.PasswordInput
    )

    def clean_password(self):
        u = auth.authenticate(
            username=self.user.username, password=self.cleaned_data["password"]
        )
        if u is None:
            raise forms.ValidationError("Your password was incorrect.")
        elif u != self.user:
            raise AssertionError(
                "Authenticated user did not match. This should be impossible."
            )
        return None  # Don't keep the password around.


class RegisterFormWithPasscode(RegisterForm):
    passcode = forms.CharField(label="passcode", max_length=200)


class UserProfileForm(forms.Form):
    username = forms.CharField(label=_("Username"), disabled=True)
    password = forms.CharField(
        label=_("Password"),
        disabled=True,
        widget=forms.PasswordInput(
            # Display a placeholder field for the user's password.
            # Obviously, we won't display their real password, since we don't
            # even know it.
            attrs={"placeholder": "●●●●●●●●"}
        ),
    )
    email = forms.EmailField(label=_("Email address"), disabled=True)


class UploadInviteFileForm(forms.Form):
    invite_file = forms.FileField()


class UploadInviteFileConfirmationForm(forms.Form):
    invite_file_contents = forms.CharField(
        label=_("Invite File Contents"), max_length=1000000
    )


class AcceptInviteForm(forms.Form):
    username = forms.CharField(label=_("Username"), required=False, disabled=True)
    email = UserEmailField(label="email", max_length=200, disabled=True)
    password = forms.CharField(
        label="password", max_length=200, widget=forms.PasswordInput
    )


class AddIPBanForm(forms.Form):
    ip = forms.CharField(label="IP Address")
    comment = forms.CharField(label="Comment", required=False)


class BanForm(forms.Form):
    target = forms.CharField(label=_("Username"), required=True)
    reason = forms.CharField(label=_("Reason"), required=True)
    days = forms.IntegerField(label=_("Days"), required=False)
    hours = forms.IntegerField(label=_("Hours"), required=False)

    def clean_target(self):
        t = self.cleaned_data["target"]
        try:
            user = models.User.objects.get(username=t)
        except models.User.DoesNotExist as e:
            raise forms.ValidationError(
                _("User %(username)s does not exist."), params={"username": t}
            ) from e
        return user

    def GetDuration(self):
        """Get the intended duration of the ban."""
        return datetime.timedelta(
            days=self.cleaned_data["days"] or 0, hours=self.cleaned_data["hours"] or 0
        )


class ClaimUsernameForm(forms.Form):
    silentselene_username = forms.CharField(
        label=_("royalflare_username"), required=True
    )
    royalflare_username = forms.CharField(label=_("royalflare_username"), required=True)


class ClaimReplaysForm(forms.Form):
    choices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        replays = kwargs.pop("replays")
        super().__init__(*args, **kwargs)
        self.fields["choices"].choices = replays.values_list("id", "id")
