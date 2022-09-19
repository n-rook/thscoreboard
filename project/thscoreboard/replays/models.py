
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
        return game_ids.GetGameName(self.game_id)

    def GetShortName(self):
        """Get a short name for this game.
        
        Someday I will figure out how to localize this. Then I will make
        English speakers get "EoSD" when Japanese speakers get "東方紅魔郷".
        """
        return game_ids.GetGameName(self.game_id, short=True)


class Shot(models.Model):

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


class ReplayStage(models.Model):
    """ Represents a stage split for a given replay
        Most games store the values from the start of the stage
        TH07 and TH08 store the values from the end of the stage
    """

    class Meta:
        constraints = [models.UniqueConstraint(fields=['replay', 'stage'], name='unique_stage_per_game')]

    replay = models.ForeignKey('Replay', on_delete=models.CASCADE)
    """The replay this split corresponds to"""

    stage = models.IntegerField()
    """ The stage this split corresponds to in the replay
        This is 0-indexed, regular stages are numbered in order, typically 0-5, extra is the stage after, usually 6
        Exceptions:
            TH08 - the A and B stages bloat the stage numbers, pushing extra back
            TH09 - there are 9 stages in main game stored as stages 0 - 8
                    the game stores the stage movement data for the AI, stored as stages 10 - 18
                    PVP is stored as a separate stage, stage 9 and 19, for player 1 and 2 respectively
                    all in all there are 40 offsets saved for potential stage data, most unused
    """

    score = models.BigIntegerField()
    """ The current score stored at this stage"""

    piv = models.IntegerField(blank=True, null=True)
    """ The current PIV stored at this stage
        This may be named as a different mechanic in some games, but it functions and is stored the same.
        Games that use this field (and the alternate names if applicable):
            TH07 - cherry
            TH10 - faith
    """

    graze = models.IntegerField(blank=True, null=True)
    """ The current graze stored at this stage
        Games that use this field:
            TH07
    """

    point_items = models.IntegerField(blank=True, null=True)
    """ The number of point items acquired at this stage
        Games that use this field:
            TH07
    """

    power = models.IntegerField(blank=True, null=True)
    """ The player's power at this stage
        In the modern windows games (TH10 onwards), the displayed power is in a different format to the stored/internal power
        The formula is (power * 0.05) and is displayed with 2 decimal places. It starts at 1.00 in some games and at 0 in others.
        Games that use this field:
            TH06
            TH07
            TH10
    """

    lives = models.IntegerField(blank=True, null=True)
    """ The number of extra lives at this stage
        Currently, all games use this field.
        (Photo games and other side games we choose to support won't)
    """

    life_pieces = models.IntegerField(blank=True, null=True)
    """ The number of life pieces at this stage
        Games that use this field:
    """

    bombs = models.IntegerField(blank=True, null=True)
    """ The number of bombs at this stage
        Games that use this field:
            TH06
            TH07
    """

    bomb_pieces = models.IntegerField(blank=True, null=True)
    """ The number of bomb pieces at this stage
        Games that use this field:
    """

    th06_rank = models.IntegerField(blank=True, null=True)
    """The internal 'rank' value for TH06"""


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
