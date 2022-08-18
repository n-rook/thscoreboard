import logging
from django.http import HttpResponseRedirect

from django.views.decorators import http as http_decorators
from django.shortcuts import render
from . import forms

@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():

            logging.info('Form was valid')
            # TODO let people register...
            return HttpResponseRedirect('./registration_success')
        else:
            pass
    else:
        form = forms.RegisterForm()

    return render(request, 'users/register.html', {'form': form})

@http_decorators.require_safe
def registration_success(request):
    return render(request, 'users/registration_success.html')

# For now, just reuse the built-in Django pages.
# @http_decorators.require_http_methods(["GET", "POST"])
# def login(request):
#     return render(request, 'users/login.html')