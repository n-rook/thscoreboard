import datetime

from django import forms
from django import http
from django.conf import settings
from django.core import exceptions
from django.views.decorators import http as http_decorators


def get_available_language_codes() -> list[str]:
    """Returns the language codes configured in settings.LANGUAGES."""
    return [code for code, _name in settings.LANGUAGES]


@http_decorators.require_http_methods(["GET", "HEAD", "POST"])
def set_language(request: http.HttpRequest):
    destination = request.META.get("HTTP_REFERER") or "/"
    resp = http.HttpResponseRedirect(destination)

    if request.method != "POST":
        return resp

    form = SetLanguageInvisibleForm(request.POST)
    if not form.is_valid():
        raise exceptions.BadRequest("Invalid form")
    lang = form.cleaned_data["language"]

    if lang not in get_available_language_codes():
        raise exceptions.BadRequest(f"Unknown language {lang}")

    destination = request.META.get("HTTP_REFERER") or "/"
    resp = http.HttpResponseRedirect(destination)
    resp.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang,
        int(datetime.timedelta(days=365).total_seconds()),
    )
    return resp


class SetLanguageInvisibleForm(forms.Form):
    """An invisible form used so users can POST their language preference."""

    language = forms.CharField()
