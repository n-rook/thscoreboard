"""Update the local version of the website."""

import logging
import subprocess
import threading

from django.core import management

try:
    import uwsgi
except ImportError:
    class uwsgi:
        def reload():
            pass


_DEPLOY_LOCK = threading.Lock()


def update_and_deploy():
    """Update the local website, and restart to pick up the update."""

    # Something weird might happen if we try to do this concurrently.
    with _DEPLOY_LOCK:
        _git_pull()

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


def _git_pull():
    # Retrieve the main branch from the github repo.
    outcome = subprocess.run(
        ['git', 'pull', '--ff-only'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True)
    logging.info('Git pull completed (exit code %d). Output:\n%s',
                 outcome.returncode, outcome.stdout)
    outcome.check_returncode()
