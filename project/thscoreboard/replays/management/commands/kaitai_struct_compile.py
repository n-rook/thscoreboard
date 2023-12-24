import logging
import subprocess
import pathlib

from django.core.management import base
import pathlib


_PROJECT_ROOT = pathlib.Path(__file__).parent / '../../..'


def _ksy_files():
    ksy_dir = _PROJECT_ROOT / pathlib.Path("../../ref/threp-ksy/")
    return [p.resolve() for p in ksy_dir.glob("*.ksy")]


class Command(base.BaseCommand):
    help = """Recompile Kaitai Struct source files."""

    def handle(*args, **options) -> None:
        ksc_args = [
                "kaitai-struct-compiler",
                "--target",
                "python",
                "--outdir",
                _PROJECT_ROOT / 'replays/kaitai_parsers',
            ] + _ksy_files()
        
        logging.info('Running: %s', ksc_args)
        subprocess.run(
            ksc_args
        )
