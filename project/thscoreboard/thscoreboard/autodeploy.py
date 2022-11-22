"""A webhook that runs "git pull" and updates the server."""

import base64
import logging
import subprocess


from django.http import HttpResponse
from django.core import management
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.views.decorators import csrf

from users.models import User


try:
    import uwsgi
except ImportError:
    class uwsgi:
        def reload():
            pass


def do_deploy():
    git_pull()

    management.call_command(
        'migrate',
        interactive=False
    )

    management.call_command(
        'setup_constant_tables',
    )

    management.call_command(
        'compilescss',
    )

    management.call_command(
        'collectstatic',
        interactive=False
    )

    uwsgi.reload()


def git_pull():
    # Retrieve the main branch from the github repo.
    outcome = subprocess.run(
        ['git', 'pull', '--ff-only'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True)
    logging.info('Git pull completed (exit code %d). Output:\n%s',
                 outcome.returncode, outcome.stdout)
    outcome.check_returncode()


@csrf.csrf_exempt
def deploy(request):
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"].split(' ')
        if len(auth) == 2 and auth[0] == "Basic":
            creds = base64.b64decode(auth[1]).decode().split(':')
            try:
                user = User.objects.get(username=creds[0])
                if check_password(creds[1], user.password) and user.is_superuser:
                    logging.info('Deploying on behalf of %s', user.username)
                    do_deploy()
                    return HttpResponse(status=200, content="Success!!!")
            except ObjectDoesNotExist:
                response = HttpResponse(status=401, content=f"Failed to authenticate user {creds[0]}")
                response.headers["WWW-Authenticate"] = "Basic"
                return response
    response = HttpResponse(status=401)
    response.headers["WWW-Authenticate"] = "Basic"
    return response
