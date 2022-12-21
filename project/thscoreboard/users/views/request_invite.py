"""Redirects to the invite form.

This page will be temporary.
"""

from django.shortcuts import redirect
from django.views.decorators import http as http_decorators


@http_decorators.require_http_methods(['GET', 'HEAD'])
def request_invite(request):
    del request  # unused
    return redirect('https://docs.google.com/forms/d/e/1FAIpQLSeyaqQRx19y0EjjAoEXlA-DLPmUAhmfWziR2qfZ_dvj1Kq_1Q/viewform')
