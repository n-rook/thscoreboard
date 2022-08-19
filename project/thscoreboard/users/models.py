from django.contrib.auth import models as auth_models
from django.db import models

# Create your models here.

class EarlyAccessPasscode(models.Model):

    passcode = models.TextField()
    """A passcode the user can supply to create an account."""


class UserPasscodeTie(models.Model):
    """Ties a user to a passcode."""

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    passcode = models.ForeignKey('users.EarlyAccessPasscode', on_delete=models.CASCADE)
