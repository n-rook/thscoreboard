import logging
from django.http import HttpResponseRedirect

from django.contrib.auth import models as auth_models
from django.db import transaction
from django.shortcuts import render
from django.views.decorators import http as http_decorators

from . import forms
from . import models


RegisterForm = forms.RegisterFormWithPasscode
_USE_PASSCODE = True


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def register(request):
    if request.method == 'POST':
        try:
            form = RegisterForm(request.POST)

            if form.is_valid():
                passcode = models.EarlyAccessPasscode.objects.get(passcode=form.cleaned_data['passcode'])
                _register(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    passcode=passcode,
                    )



                logging.info('Form was valid')


                # TODO let people register...
                return HttpResponseRedirect('./registration_success')
            
        except models.EarlyAccessPasscode.DoesNotExist:
            form.add_error('passcode', 'Early access; must provide a valid passcode')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {
        'form': form,
        'require_passcode': _USE_PASSCODE
        })


@transaction.atomic
def _register(username, password, email, passcode):
    u = auth_models.User.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    tie = models.UserPasscodeTie(user=u, passcode=passcode)
    tie.save()


@http_decorators.require_safe
def registration_success(request):
    return render(request, 'users/registration_success.html')

# For now, just reuse the built-in Django pages.
# @http_decorators.require_http_methods(["GET", "POST"])
# def login(request):
#     return render(request, 'users/login.html')