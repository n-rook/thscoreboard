from django.contrib.auth import models as auth_models
from django.db import models

from thscoreboard import settings

# Create your models here.


class User(auth_models.AbstractUser):
    """A user."""

    class Meta(auth_models.AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint('email', name='unique_email')
        ]

class EarlyAccessPasscode(models.Model):

    passcode = models.TextField()
    """A passcode the user can supply to create an account."""


class UserPasscodeTie(models.Model):
    """Ties a user to a passcode."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    passcode = models.ForeignKey('users.EarlyAccessPasscode', on_delete=models.CASCADE)
