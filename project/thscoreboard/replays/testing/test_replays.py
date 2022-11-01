"""Makes some replays available for tests."""

from os import path
import typing


_filename_type = typing.Literal['th6_extra', 'th6_hard_1cc', 'th7_lunatic', 'th10_normal']
"""A special literal type which defines all possible filenames.

Why bother with this? Well, it gets most IDEs to autocomplete these values,
which is very convenient!
"""


def GetRaw(filename: _filename_type) -> bytes:
    """Read and return a test replay as bytes.

    Args:
        filename: The first part of the filename (before ".rpy").

    Returns:
        The file, in bytes.
    """
    true_filename = f'{filename}.rpy'

    with open(path.join('replays/replays_for_tests', true_filename), 'rb') as f:
        return f.read()
