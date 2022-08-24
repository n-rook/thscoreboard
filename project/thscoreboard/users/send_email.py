"""Contains functions that send specific email messages."""
from urllib import parse


from django.core import mail
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django import urls

from thscoreboard import settings
from . import models


_ACCOUNTS_EMAIL = 'accounts@silentselene.net'


def _GetFullyQualifiedLink(request, url_path: str):
    site = get_current_site(request)
    if settings.USE_HTTPS_IN_EMAIL_LINKS:
        scheme = 'https'
    else:
        scheme = 'http'

    return parse.urlunparse((
        scheme,
        site.domain,
        url_path,
        None,
        None,
        None
    ))


def SendVerificationEmail(request, u: models.UnverifiedUser):
    full_link = _GetFullyQualifiedLink(
        request,
        urls.reverse('users:verify_email', kwargs={'token': u.token})
    )

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
