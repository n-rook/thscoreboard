"""A route used for webhooks that deploys the server."""

import base64
import logging

from django import http
from django.contrib.auth import hashers
from django.views.decorators import csrf

from thscoreboard.deploy import deploy as deploy_lib
from users import models


@csrf.csrf_exempt
def deploy(request):
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"].split(' ')
        if len(auth) == 2 and auth[0] == "Basic":
            creds = base64.b64decode(auth[1]).decode().split(':')
            try:
                user = models.User.objects.get(username=creds[0])
                if hashers.check_password(creds[1], user.password) and user.is_superuser:
                    logging.info('Deploying on behalf of %s', user.username)
                    deploy_lib.update_and_deploy(user.username)
                    return http.HttpResponse(status=200, content="Success!!!")
            except models.User.DoesNotExist:
                response = http.HttpResponse(status=401, content=f"Failed to authenticate user {creds[0]}")
                response.headers["WWW-Authenticate"] = "Basic"
                return response
    response = http.HttpResponse(status=401)
    response.headers["WWW-Authenticate"] = "Basic"
    return response
