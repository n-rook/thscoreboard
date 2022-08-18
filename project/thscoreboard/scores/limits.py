
from django.core.exceptions import ValidationError

MAX_REPLAY_SIZE = 1000000

class FileTooBigError(ValidationError):
    """Raised if a replay is too big."""

    def __init__(self):
        super().__init__('Replays cannot be bigger than 1MB.')

