import logging
from django.http import HttpResponseRedirect

from django.views.decorators import http as http_decorators
from django.shortcuts import render
from . import forms

# Create your views here.

@http_decorators.require_http_methods(["GET", "POST"])
def login(request):
    return render(request, 'users/login.html')

@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            logging.info('Form was valid')
            return HttpResponseRedirect('./registration_success')
        else:
            pass
    else:
        form = forms.RegisterForm()

    return render(request, 'users/register.html', {'form': form})
    

    # if request.method == 'POST':
    #     new_username = request.POST.get('username')
    #     new_password = request.POST.get('password')
    #     new_email = request.POST.get('email')
    #     logging.info('%s %s %s', new_username, new_email, new_password)
        

    # return render(request, 'users/register.html')

def registration_success(request):
    return render(request, 'users/registration_success.html')
