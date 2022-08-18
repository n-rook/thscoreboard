
from django.db import models

from . import limits

class Game(models.Model):
    game_id = models.TextField(primary_key=True)
    """A unique ID for the game, based on its number.
    
    For example, Touhou 6 is th06.
    """

    has_replays = models.BooleanField()
    """Whether the game supports replay files."""


class Shot(models.Model):

    shot_id = models.TextField()
    """A unique ID for the shot.

    Typically, this is the name of the character (in English), plus perhaps a
    letter. For example, Touhou 6 contains "ReimuA", "ReimuB", "MarisaA" and
    "MarisaB".
    """

    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    """The game in which this shot appears."""

    class Meta:
        constraints = [models.UniqueConstraint('shot_id', 'game', name='unique_shot_per_game')]


# Create your models here.
class Score(models.Model):
    """Represents a score recorded on the scoreboard."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    """The user who uploaded the replay."""

    # game = models.ForeignKey('Game', on_delete=models.PROTECT)
    # """The game this replay comes from."""
    # This is denormalized! Just get it from "shot".

    shot = models.ForeignKey('Shot', on_delete=models.PROTECT)
    """The shot type the player used."""

    score = models.BigIntegerField()
    """The score of the replay."""

    video_url = models.TextField(max_length=1000)
    """A URL to a video site with a recording of the run."""
    

class ReplayFile(models.Model):
    """Represents a replay file for a given score."""

    score = models.OneToOneField('Score', on_delete=models.CASCADE)
    """The score record to which this replay corresponds."""

    is_good = models.BooleanField()
    """Whether a replay file can be used unmodified to watch the replay.
    
    Even a desynced replay file can be useful to have. For example, maybe the
    Touhou community will later discover how to fix a certain type of desync.
    """

class TemporaryReplayFile(models.Model):
    """Represents a temporarily held replay file a user is uploading.
    
    When the user is uploading a replay file, we want the server to receive the
    file and parse metadata from it to help the user. However, this means that the
    replay must be saved before it is published.
    """

    # TODO: When this table gets big, we can bother with a good way to clean it up.
    # But replay files are not that big, so let's deal with that later.

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    """When the replay file was uploaded."""

    replay = models.BinaryField(max_length=limits.MAX_REPLAY_SIZE)
    """The replay file itself."""
