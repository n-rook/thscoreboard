"""This view lets a user delete their own account."""

from django.shortcuts import render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators

from users import forms
from users.middleware import check_ban


@auth_decorators.login_required
@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
@check_ban.allow_access_by_banned_users
def delete_account(request):
    if request.method == "POST":
        form = forms.DeleteAccountForm(request.user, request.POST)
        if form.is_valid():
            request.user.MarkForDeletion()
            request.user.save()
            return render(request, "users/delete_account_successful.html")
    else:
        form = forms.DeleteAccountForm(request.user)

    return render(request, "users/delete_account.html", {"form": form})
