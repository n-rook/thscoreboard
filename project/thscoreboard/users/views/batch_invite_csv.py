"""Views related to batch-inviting users via CSV."""

import logging

from django.shortcuts import redirect, render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators

from users import forms
from users import models
from users import parse_invite_csv
from users import send_email


@auth_decorators.login_required
@auth_decorators.permission_required("staff", raise_exception=True)
@http_decorators.require_http_methods(["GET", "HEAD"])
def batch_invite(request):
    return render(
        request,
        "users/batch_invite_upload.html",
        {"form": forms.UploadInviteFileForm()},
    )


@auth_decorators.login_required
@auth_decorators.permission_required("staff", raise_exception=True)
@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def batch_invite_confirm(request):
    if request.method == "POST":
        button_value = request.POST.get("submit-button", "")
        if not button_value:
            print("not button value")
            return redirect("users:batch_invite")

        elif button_value == "Upload":
            _ = forms.UploadInviteFileForm(request.POST, request.FILES)

            if "invite_file" in request.FILES:
                invite_file = request.FILES["invite_file"]
                file_contents = invite_file.read()
                str_contents = file_contents.decode("utf-8")
                parsed_csv = parse_invite_csv.Parse(str_contents)

                confirm_form = forms.UploadInviteFileConfirmationForm(
                    initial={
                        "invite_file_contents": str_contents,
                    }
                )

                return render(
                    request,
                    "users/batch_invite_confirm.html",
                    {
                        "form": confirm_form,
                        "invite_rows": parsed_csv,
                        "is_error": any([not True for r in parsed_csv]),
                    },
                )

        elif button_value == "Confirm":
            confirm_form = forms.UploadInviteFileConfirmationForm(
                request.POST, request.FILES
            )
            if confirm_form.is_valid():
                parsed_csv = parse_invite_csv.Parse(
                    confirm_form.cleaned_data["invite_file_contents"]
                )

                for r in parsed_csv:
                    if r.errors:
                        logging.info(
                            "Parsed CSV had errors; not uploading.",
                            parsed_csv.errors_str,
                        )
                        raise Exception(parsed_csv.errors_str)

                for r in parsed_csv:
                    CreateInvitedUserAndSendEmail(r, request.user)

                return render(
                    request,
                    "users/batch_invite_success.html",
                    {
                        "count": len(parsed_csv),
                    },
                )
            else:
                raise Exception("Not valid :/")

    return redirect("users:batch_invite")


def CreateInvitedUserAndSendEmail(row: parse_invite_csv.Parse, inviter: models.User):
    invited = models.InvitedUser.CreateInvite(row.username, row.email, inviter)
    send_email.SendInviteEmail(invited)
