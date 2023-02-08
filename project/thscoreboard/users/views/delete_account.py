"""This view lets a user delete their own account."""

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators
from django.core.exceptions import ValidationError

from users import forms

@auth_decorators.login_required
@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def delete_account(request):
    if request.method == 'POST':
        form = forms.DeleteAccountForm(request.user, request.POST)
        if form.is_valid():
            raise ValueError('not implemented')
    else:
        form = forms.DeleteAccountForm(request.user)

    return render(
        request,
        'users/delete_account.html',
        {
            'form': form
        }
    )
