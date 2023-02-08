
import datetime
from typing import Any, Optional

from django import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

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

        if models.User.objects.filter(username=value):
            raise exceptions.ValidationError(
                _('An account has already been registered with this username.'))


class UserEmailField(forms.EmailField):

    def to_python(self, value: Optional[Any]) -> Optional[str]:
        value = super().to_python(value)
        if value is None:
            return None

        return models.User.normalize_email(value)

    def validate(self, value):
        if value is None:
            return True

        if models.User.objects.filter(email=value):
            raise exceptions.ValidationError(
                _('An account has already been registered with this email address.'))


class RegisterForm(forms.Form):
    # username = forms.CharField(label='username', max_length=100)
    username = UsernameField(label='username', max_length=30)
    # email = forms.EmailField(label='email', max_length=200)
    email = UserEmailField(label='email', max_length=200)
    password = forms.CharField(label='password', max_length=200, widget=forms.PasswordInput)


class RegisterFormWithPasscode(RegisterForm):
    passcode = forms.CharField(label='passcode', max_length=200)


class UserProfileForm(forms.Form):
    username = forms.CharField(label=_('Username'), disabled=True)
    password = forms.CharField(
        label=_('Password'),
        disabled=True,
        widget=forms.PasswordInput(
            # Display a placeholder field for the user's password.
            # Obviously, we won't display their real password, since we don't
            # even know it.
            attrs={'placeholder': '●●●●●●●●'}
        ))
    email = forms.EmailField(label=_('Email address'), disabled=True)


class UploadInviteFileForm(forms.Form):
    invite_file = forms.FileField()


class UploadInviteFileConfirmationForm(forms.Form):
    invite_file_contents = forms.CharField(label=_('Invite File Contents'), max_length=1000000)


class AcceptInviteForm(forms.Form):
    username = forms.CharField(label=_('Username'), required=False, disabled=True)
    email = UserEmailField(label='email', max_length=200, disabled=True)
    password = forms.CharField(label='password', max_length=200, widget=forms.PasswordInput)


class AddIPBanForm(forms.Form):
    ip = forms.CharField(label='IP Address')
    comment = forms.CharField(label='Comment', required=False)


class BanForm(forms.Form):
    target = forms.CharField(label=_('Username'), required=True)
    reason = forms.CharField(label=_('Reason'), required=True)
    days = forms.IntegerField(label=_('Days'), required=False)
    hours = forms.IntegerField(label=_('Hours'), required=False)

    def clean_target(self):
        t = self.cleaned_data['target']
        try:
            user = models.User.objects.get(username=t)
        except models.User.DoesNotExist as e:
            raise forms.ValidationError(
                _('User %(username)s does not exist.'),
                params={'username': t}) from e
        return user

    def GetDuration(self):
        """Get the intended duration of the ban."""
        return datetime.timedelta(
            days=self.cleaned_data['days'] or 0,
            hours=self.cleaned_data['hours'] or 0)
