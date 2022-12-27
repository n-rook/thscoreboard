"""Defines views for user and account management."""
# TODO: Separate views in different files and put in views/.

from typing import Optional
from django.http import HttpResponseRedirect, HttpResponseForbidden
from ipaddress import ip_address, ip_network
from functools import wraps

from django.contrib import auth
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators import http as http_decorators

from . import send_email
from . import forms
from . import models


RegisterForm = forms.RegisterFormWithPasscode
_USE_PASSCODE = True


def check_ip_bans(methods_to_check: list):
    def is_ip_banned(ip_to_check: str):
        request_ip = ip_address(ip_to_check)
        return any(request_ip in ip_network(ip.ip) for ip in models.IPBan.objects.all())

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method in methods_to_check and is_ip_banned(request.META.get('REMOTE_ADDR')):
                return HttpResponseForbidden(content='Your IP address is banned')
            return func(request, *args, **kwargs)
        return inner
    return decorator


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
@check_ip_bans(["POST"])
def register(request):
    """Start trying to register an account.

    The account registration flow works as follows:

    1. The user visits /register and sees a registration form, asking for a
       username, password and email address.
    2. If the user's selected username and email are not used by actual users,
       we add them to the "unverified_users" table, then send them an email.
       unverified_users are NOT real users; they do not block other users from
       registering with the given username or email address, and there are no
       unique columns on unverified_users. This means that username is not a
       primary key of this table.
    3. We send an email to the email address in question with a link to an
       "email verification" page, containing the primary key for their
       unverified_users user.
    4. If the user clicks that page, they see a confirmation page because
       I don't want to confirm somebody's account with a GET.
    5. If they POST there, they get a real account.
    6. TODO: We set up a cleanup cron job to delete temporary users so that we
       are not indefinitely holding these rows.

    TODO: If a user tries to log in as an unverified user, we should resend
    the notification email, even though they cannot log in yet.
    """
    if request.method == 'POST':
        try:
            form = RegisterForm(request.POST)

            if form.is_valid():
                passcode = models.EarlyAccessPasscode.objects.get(passcode=form.cleaned_data['passcode'])
                unverified_user = _preregister(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    passcode=passcode)
                send_email.SendVerificationEmail(request, unverified_user)
                return HttpResponseRedirect('./preregistered')

        except models.EarlyAccessPasscode.DoesNotExist:
            form.add_error('passcode', 'Early access; must provide a valid passcode')
    else:
        form = RegisterForm()

    return render(
        request, 'users/register.html',
        {
            'form': form,
            'require_passcode': _USE_PASSCODE
        })


@transaction.atomic
def _preregister(username, password, email, passcode: Optional[str]):
    # Create an unverified user.
    unverified_user = models.UnverifiedUser.CreateUser(username=username, email=email, raw_password=password)
    if passcode is not None:
        tie = models.UserPasscodeTie(unverified_user=unverified_user, passcode=passcode)
        tie.save()
    return unverified_user


@transaction.atomic
def _register(username, password, email, passcode):
    u = auth.get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email
    )
    tie = models.UserPasscodeTie(user=u, passcode=passcode)
    tie.save()


def preregistered(request):
    return render(request, 'users/preregistered.html')


@http_decorators.require_safe
def registration_success(request):
    return render(request, 'users/registration_success.html')


@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def verify_email(request, token: str):
    try:
        unverified_user = models.UnverifiedUser.objects.get(token=token)
    except models.UnverifiedUser.DoesNotExist:
        return render(request, 'users/verify_email.html', {
            'unverified_user': None
        })

    if request.method == 'POST':
        new_account = unverified_user.VerifyUser()
        # Log the user in.
        # Note that this does mean a user with access to the confirmation email
        # gets to log in. But if they have the user's email account, they could
        # just do a forgot password anyway.
        auth.login(request, new_account)
        return redirect('users:registration_success')

    return render(request, 'users/verify_email.html', {
        # TODO: It would be nice to tell the user if it's too late and they are doomed.
        'unverified_user': unverified_user,
    })
