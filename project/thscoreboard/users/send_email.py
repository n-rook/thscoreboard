"""Contains functions that send specific email messages."""

from django.core import mail
from django.template import loader
from django import urls

from thscoreboard import settings
from . import models


_ACCOUNTS_EMAIL = 'Silent Selene Accounts <accounts@silentselene.net>'


def SendVerificationEmail(request, u: models.UnverifiedUser):
    full_link = settings.SITE_BASE + '/' + urls.reverse('users:verify_email', kwargs={'token': u.token})

    text_message = loader.render_to_string(
        'registration/email/verification.txt',
        context={
            'site_name': 'Silent Selene',
            'link': full_link
        }
    )
    email = mail.EmailMessage(
        subject='Register your account at Silent Selene',
        body=text_message,
        from_email=_ACCOUNTS_EMAIL,
        to=[u.email],
    )
    email.send()
