
from django.db import models
from django.contrib import auth

from thscoreboard import settings

from . import game_ids
from . import limits


class Game(models.Model):

    class Meta:
        ordering = ['game_id']

    game_id = models.TextField(primary_key=True)
    """A unique ID for the game, based on its number.
    
    For example, Touhou 6 is th06.
    """

    has_replays = models.BooleanField()
    """Whether the game supports replay files."""

    num_difficulties = models.IntegerField()
    """The number of difficulties the game has.
    
    For the vast majority of Touhou games, this is 5: Easy, Normal, Hard,
    Lunatic, and Extra.

    The difficulties will be given numeric values in actual replay rows,
    starting from 0.
    """

    def GetName(self):
        """Get a long name for the game."""
        return game_ids.GetGameName(self.game_id)

    def GetShortName(self):
        """Get a short name for this game, suitable for a column in a table."""
        return game_ids.GetGameName(self.game_id, short=True)


class Shot(models.Model):
    """The character selected by the player.
    
    If a game has both "shots" and "subshots", this includes both. For example,
    in EoSD, Reimu has two Shot rows, "ReimuA" and "ReimuB".

    All games have shots. (This makes a lot of code simpler, since it can
    assume the presence of a shot type.) If a game does not let the player
    select a shot, a single row is defined, named after the protagonist.
    """

    class Meta:
        constraints = [models.UniqueConstraint('shot_id', 'game', name='unique_shot_per_game')]

    shot_id = models.TextField()
    """A unique ID for the shot.

    Typically, this is the name of the character (in English), plus perhaps a
    letter. For example, Touhou 6 contains "ReimuA", "ReimuB", "MarisaA" and
    "MarisaB".
    """

    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    """The game in which this shot appears."""

    def GetName(self):
        """Get a pretty name for this shot type. Note: Populates game."""
        return game_ids.GetShotName(self.game.game_id, self.shot_id)
    

class Category(models.IntegerChoices):
    REGULAR = 1
    TAS = 2
    UNLISTED = 3
    PRIVATE = 4


class Route(models.Model):
    """One of several sets of stages pickable by the player in a run.
    
    For example, Imperishable Night has two routes: "Final A" and "Final B".

    The route has to be chosen by the player for the route; for example,
    the two Stage 4s of IN don't count, because each shot can only face one
    stage.

    Most games do not have different routes, so they do not have rows in this
    table.
    """

    class Meta:
        constraints = [models.UniqueConstraint('route_id', 'game', name='unique_route_per_game')]

    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    """The game in which this shot appears."""

    route_id = models.TextField()
    """A unique ID for the route."""

    order_number = models.IntegerField()
    """A number used only to order the routes in a game.
    
    For example, if two routes have 1 and 2, the route with 1 is listed first,
    then the route with 2.
    """

    def GetName(self):
        """Get a pretty name for this route. Populates the game field."""
        return game_ids.GetRouteName(self.game.game_id, self.route_id)


# Create your models here.
class Replay(models.Model):

    class Meta:
        ordering = ['shot', 'difficulty', '-points']

        constraints = [
            models.CheckConstraint(
                check=models.Q(difficulty__gte=0),
                name='difficulty_gte_0'
            ),
        ]

    """Represents a score recorded on the scoreboard."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    """The user who uploaded the replay."""

    category = models.IntegerField(choices=Category.choices)

    created = models.DateTimeField(auto_now_add=True)
    """When the replay was uploaded."""

    shot = models.ForeignKey('Shot', on_delete=models.PROTECT)
    """The shot type the player used."""

    difficulty = models.IntegerField()
    """The difficulty on which the player played."""

    route = models.ForeignKey('Route', on_delete=models.PROTECT, blank=True, null=True)
    """The route on which the game was played."""
    
    def GetDifficultyName(self):
        """Get a pretty name for this difficulty. Note: Populates shot and game."""
        return game_ids.GetDifficultyName(self.shot.game.game_id, self.difficulty)
    
    def GetDifficultyUrlCode(self):
        return f'd{self.difficulty}'

    points = models.BigIntegerField()
    """The score of the replay."""
    
    is_good = models.BooleanField(blank=True, null=True)
    """Whether a replay file can be used unmodified to watch the replay.
    
    Even a desynced replay file can be useful to have. For example, maybe the
    Touhou community will later discover how to fix a certain type of desync.

    If this submission has no replay file, this field will be null.
    """

    rep_points = models.BigIntegerField(blank=True, null=True)
    """The final score recorded in the replay.
    
    This will usually be the same as the score on the Score row, but in some
    cases it will be different. For example, this will be the max score for
    counterstop replays.

    If this submission has no replay file, this field will be null.
    """

    video_link = models.TextField(max_length=1000)
    """A URL to a video site with a recording of the run."""

    comment = models.TextField(max_length=limits.MAX_COMMENT_LENGTH)
    """A comment the user entered."""

    timestamp = models.DateTimeField(blank=True, null=True)
    """Timestamp from the replay"""

    def IsVisible(self, viewer: auth.get_user_model()):
        """Returns whether this replay should be visible to this user."""
        # Add a unit test for this

        if self.category != Category.PRIVATE:
            return True
        return self.user == viewer

    def GetNiceFilename(self, ascii_only=False):
        """Returns a nice filename for this replay.
        
        This always returns something, even if this submission does not actually
        have a replay file.

        Args:
            ascii_only: If True, don't include the username, so that this can
            safely be included in a "filename" Content-Disposition field.
        """
        return '{gamecode}_{user}_{id}.rpy'.format(
            gamecode=self.shot.game.game_id,
            user=self.user.username,
            id=self.id,
        )


class ReplayFile(models.Model):
    """Represents a replay file for a given score."""

    replay = models.OneToOneField('Replay', on_delete=models.CASCADE)
    """The submission to which this replay corresponds."""

    replay_file = models.BinaryField(max_length=limits.MAX_REPLAY_SIZE, blank=True, null=True)
    """The replay file itself."""


class TemporaryReplayFile(models.Model):
    """Represents a temporarily held replay file a user is uploading.
    
    When the user is uploading a replay file, we want the server to receive the
    file and parse metadata from it to help the user. However, this means that the
    replay must be saved before it is published.
    """

    # TODO: When this table gets big, we can bother with a good way to clean it up.
    # But replay files are not that big, so let's deal with that later.

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    """When the replay file was uploaded."""

    replay = models.BinaryField(max_length=limits.MAX_REPLAY_SIZE)
    """The replay file itself."""
