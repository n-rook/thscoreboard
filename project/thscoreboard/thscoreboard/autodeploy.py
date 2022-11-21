"""A webhook that runs "git pull" and updates the server."""

import base64
import logging
import subprocess

from sass_processor.management.commands import compilescss

from django.http import HttpResponse
from django.contrib.staticfiles.management.commands import collectstatic
from django.core.management.commands import migrate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.views.decorators import csrf

from users.models import User
from replays.management.commands import setup_constant_tables


try:
    import uwsgi
except ImportError:
    class uwsgi:
        def reload():
            pass


def do_deploy():
    git_pull()

    migrate.Command().handle(
        database="default",
        skip_checks=False,
        verbosity=1,
        interactive=False,
        run_syncdb=False,
        app_label="",
        prune="",
        plan=""
    )
    setup_constant_tables.SetUpConstantTables()
    compilescss.Command().handle(
        verbosity=1,
        delete_files=False,
        use_storage=False,
        sass_precision=True
    )
    collectstatic.Command().handle(
        interactive=False,
        verbosity=1,
        link=False,
        clear=True,
        dry_run=False,
        ignore_patterns=[],
        use_default_ignore_patterns=False,
        post_process=False
    )
    uwsgi.reload()


def git_pull():
    # Retrieve the main branch from the github repo.
    outcome = subprocess.run(
        ['git', 'pull', '--ff-only'],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True)
    logging.info('Pulled recent changes from origin.\nOutput:\n%s', outcome.stdout)


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
