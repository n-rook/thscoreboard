#!/usr/bin/env python3
"""Deploy a checkout and announce the result to Discord.

This script deliberately has no Django dependency.  Run it under the dedicated
deployment account, not under the account that serves uWSGI.
"""

import argparse
import json
import logging
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Sequence
from urllib import error, request


DEFAULT_GITHUB_REPOSITORY = "n-rook/thscoreboard"
DEFAULT_BRANCH = "main"
DJANGO_DIRECTORY = Path("project/thscoreboard")
LOGGER = logging.getLogger(__name__)


def run_git(repository: Path, *arguments: str) -> None:
    """Run a Git command in repository."""
    command = ["git", "-C", str(repository), *arguments]
    LOGGER.info("Running %s", shlex.join(command))
    subprocess.run(command, check=True)


def head_revision(repository: Path) -> str:
    """Return the current Git revision in repository."""
    command = ["git", "-C", str(repository), "rev-parse", "HEAD"]
    LOGGER.info("Running %s", shlex.join(command))
    result = subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def run_manage(repository: Path, *arguments: str) -> None:
    """Run one Django management command from the checkout virtualenv."""
    django_directory = repository / DJANGO_DIRECTORY
    python = repository / ".venv/bin/python"
    if not django_directory.is_dir():
        raise ValueError(f"Django directory does not exist: {django_directory}")
    if not python.is_file():
        raise ValueError(f"Virtualenv Python does not exist: {python}")

    command = [str(python), "manage.py", *arguments]
    LOGGER.info("Running %s", shlex.join(command))
    subprocess.run(command, cwd=django_directory, check=True)


def get_webhook_url() -> str:
    """Get a Discord webhook URL from the deployment service environment."""
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url:
        return webhook_url

    webhook_id = os.environ.get("DISCORD_WEBHOOK_ID")
    webhook_token = os.environ.get("DISCORD_WEBHOOK_TOKEN")
    if webhook_id and webhook_token:
        return "https://discord.com/api/webhooks/{}/{}".format(
            webhook_id, webhook_token
        )

    raise RuntimeError(
        "Set DISCORD_WEBHOOK_URL or both DISCORD_WEBHOOK_ID and "
        "DISCORD_WEBHOOK_TOKEN."
    )


def announce(webhook_url: str, message: str) -> None:
    """Send message to a Discord incoming webhook."""
    LOGGER.info("Sending Discord deployment notification.")
    payload = json.dumps({"content": message}).encode("utf-8")
    discord_request = request.Request(
        f"{webhook_url}?wait=true",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(discord_request, timeout=15) as response:
            if not 200 <= response.status < 300:
                raise RuntimeError(f"Discord returned HTTP {response.status}")
    except error.HTTPError as exc:
        raise RuntimeError(f"Discord returned HTTP {exc.code}") from exc
    except error.URLError as exc:
        raise RuntimeError("Could not reach Discord") from exc
    LOGGER.info("Discord deployment notification sent.")


def update(
    repository: Path,
    branch: str,
    github_repository: str,
    announce_update: bool,
) -> None:
    """Perform every step in the legacy deployment flow."""
    if not repository.is_dir():
        raise ValueError(f"Repository directory does not exist: {repository}")

    LOGGER.info("Starting deployment for %s.", repository)
    old_revision = head_revision(repository)
    run_git(repository, "pull", "--ff-only", "origin", branch)
    new_revision = head_revision(repository)

    if new_revision == old_revision:
        LOGGER.info(
            "%s is already at %s; running deployment steps.", repository, new_revision
        )
    else:
        LOGGER.info(
            "Updated %s from %s to %s.", repository, old_revision, new_revision
        )

    run_manage(repository, "migrate", "--noinput")
    run_manage(repository, "setup_constant_tables")
    run_manage(repository, "compilescss")
    run_manage(repository, "compilemessages")
    run_manage(repository, "collectstatic", "--noinput")

    if announce_update:
        message = (
            f"Updated to commit {new_revision}:\n"
            f"https://github.com/{github_repository}/commit/{new_revision}"
        )
        announce(get_webhook_url(), message)
    else:
        LOGGER.info("Discord notification disabled for this deployment.")

    LOGGER.info("Deployment steps completed; systemd will reload the Web service.")


def parse_args(arguments: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository",
        required=True,
        type=Path,
        help="Path to the existing Git checkout to update.",
    )
    parser.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help="Remote branch to deploy (default: main).",
    )
    parser.add_argument(
        "--github-repository",
        default=DEFAULT_GITHUB_REPOSITORY,
        help="GitHub owner/repository used in the commit link.",
    )
    parser.add_argument(
        "--no-announce",
        action="store_false",
        dest="announce_update",
        help="Deploy without sending a Discord message.",
    )
    return parser.parse_args(arguments)


def main(arguments: Sequence[str]) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    args = parse_args(arguments)
    try:
        update(
            repository=args.repository,
            branch=args.branch,
            github_repository=args.github_repository,
            announce_update=args.announce_update,
        )
    except (OSError, subprocess.CalledProcessError, RuntimeError, ValueError) as exc:
        LOGGER.exception("Deployment failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
