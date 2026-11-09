#!/usr/bin/env python3
"""Check whether a checkout can fast-forward to a remote branch.

Install this script as a root-owned file outside the application checkout.
It is run by the deployment account from a systemd ExecCondition.
"""

import argparse
import logging
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Sequence


LOGGER = logging.getLogger(__name__)


def git_output(repository: Path, *arguments: str) -> str:
    """Run Git and return its standard output."""
    command = ["git", "-C", str(repository), *arguments]
    LOGGER.info("Running %s", shlex.join(command))
    result = subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def check_for_update(repository: Path, branch: str) -> bool:
    """Fetch branch and report whether it is a fast-forward update."""
    if not repository.is_dir():
        raise ValueError(f"Repository directory does not exist: {repository}")

    local_revision = git_output(repository, "rev-parse", "--verify", "HEAD")
    git_output(repository, "fetch", "--quiet", "origin", branch)
    remote_revision = git_output(repository, "rev-parse", "--verify", "FETCH_HEAD")

    if remote_revision == local_revision:
        LOGGER.info("No update: %s is already at %s.", repository, local_revision)
        return False

    command = [
        "git",
        "-C",
        str(repository),
        "merge-base",
        "--is-ancestor",
        local_revision,
        remote_revision,
    ]
    LOGGER.info("Running %s", shlex.join(command))
    result = subprocess.run(command, check=False)
    if result.returncode == 0:
        LOGGER.info(
            "Update available for %s: %s -> %s.",
            repository,
            local_revision,
            remote_revision,
        )
        return True
    if result.returncode == 1:
        raise RuntimeError(
            "Staging HEAD is not an ancestor of the fetched remote branch; "
            "refusing to deploy."
        )
    raise subprocess.CalledProcessError(result.returncode, command)


def parse_args(arguments: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository",
        required=True,
        type=Path,
        help="Path to the Git checkout to check.",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Remote branch to compare with HEAD (default: main).",
    )
    return parser.parse_args(arguments)


def main(arguments: Sequence[str]) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    args = parse_args(arguments)
    try:
        return 0 if check_for_update(args.repository, args.branch) else 1
    except (OSError, RuntimeError, subprocess.CalledProcessError, ValueError) as exc:
        LOGGER.exception("Update check failed: %s", exc)
        # ExecCondition treats 1 through 254 as a normal skip.  Exit 255 so
        # systemd marks Git and repository errors as an actual failure.
        return 255


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
