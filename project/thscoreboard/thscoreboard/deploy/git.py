"""Run Git commands in subprocesses."""

import logging
import subprocess


def pull():
    """Update the current branch from the remote repository."""

    outcome = subprocess.run(
        ['git', 'pull', '--ff-only'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True)
    logging.info('Git pull completed (exit code %d). Output:\n%s',
                 outcome.returncode, outcome.stdout)
    outcome.check_returncode()


def head_revision() -> str:
    """Return the HEAD revision."""

    outcome = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        capture_output=True,
        check=True,
        text=True
    )
    # The output from Git has a newline, so we must strip it.
    return outcome.stdout.strip()
