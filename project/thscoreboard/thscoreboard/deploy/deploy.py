"""Update the local version of the website."""

import threading

from django.core import management

from thscoreboard.deploy import discord_announce
from thscoreboard.deploy import git
from thscoreboard.deploy import uwsgi


_DEPLOY_LOCK = threading.Lock()


def update_and_deploy(user: str):
    """Update the local website, and restart to pick up the update."""

    # Something weird might happen if we try to do this concurrently.
    with _DEPLOY_LOCK:
        git.pull()

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

        revision = git.head_revision()
        discord_announce.announce(
            '{user} updated to commit {rev}:\n{rev_link}'.format(
                user=user,
                rev=revision,
                rev_link=_get_github_link(revision),
            )
        )

        uwsgi.reload()


def _get_github_link(revision):
    """Get a link to GitHub for a given revision."""
    return f'https://github.com/n-rook/thscoreboard/commit/{revision}'
