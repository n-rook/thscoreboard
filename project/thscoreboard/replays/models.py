
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
        ordering = ['shot', 'rep_difficulty', '-points']

        constraints = [
            models.CheckConstraint(
                check=models.Q(rep_difficulty__gte=0),
                name='difficulty_gte_0'
            ),
        ]

    """Represents a score recorded on the scoreboard."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    """The user who uploaded the replay."""

    #   submission related metadata

    category = models.IntegerField(choices=Category.choices)

    created = models.DateTimeField(auto_now_add=True)
    """When the replay was uploaded."""

    comment = models.TextField(max_length=limits.MAX_COMMENT_LENGTH)
    """A comment the user entered."""

    points = models.BigIntegerField()
    """The final score of the run. If the run counterstops, this value should contain the post-counterstop score"""

    #   replay metadata

    shot = models.ForeignKey('Shot', on_delete=models.PROTECT)
    """The shot type the player used."""

    rep_date = models.DateTimeField()
    """
        What to do about replays that don't store year
        Just have the user enter it manually I guess
    """

    rep_points = models.BigIntegerField()
    """ The final score recorded in the replay.
    
        This will usually be the same as the score on the Score row, but in some
        cases it will be different. For example, this will be the max score for
        counterstop replays.
    """

    rep_name = models.TextField()
    
    rep_difficulty = models.IntegerField()
    """The difficulty on which the player played."""
    
    def GetDifficultyName(self):
        """Get a pretty name for this difficulty. Note: Populates shot and game."""
        return game_ids.GetDifficultyName(self.shot.game.game_id, self.rep_difficulty)
    
    def GetDifficultyUrlCode(self):
        return f'd{self.difficulty}'

    rep_slowdown = models.FloatField(blank=True, null=True)

    rep_clear = models.IntegerField(blank=True, null=True)

    rep_spellpracticeid = models.IntegerField(blank=True, null=True)

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

class ReplayStages(models.Model):

    class Meta:
        constraints = [models.UniqueConstraint('replay', 'stage', name='unique_stage_per_replay')]

    replay = models.OneToOneField('Replay', on_delete=models.CASCADE, primary_key=True)   

    stage = models.IntegerField()

    power = models.IntegerField(blank=True, null=True)

    piv = models.IntegerField(blank=True, null=True)

    lives = models.IntegerField(blank=True, null=True)

    life_pieces = models.IntegerField(blank=True, null=True)

    bombs = models.IntegerField(blank=True, null=True)

    bomb_pieces = models.IntegerField(blank=True, null=True)

    graze = models.IntegerField(blank=True, null=True)

    point_items = models.IntegerField(blank=True, null=True)

    """Game specific entries"""

    
    th06_rank = models.IntegerField(blank=True, null=True)

    th07_cherry = models.IntegerField(blank=True, null=True)

    th07_cherrymax = models.IntegerField(blank=True, null=True)

    th08_time = models.IntegerField(blank=True, null=True)

    th08_human_youkai = models.IntegerField(blank=True, null=True)

    th09_char = models.IntegerField(blank=True, null=True)

    th09_ai = models.IntegerField(blank=True, null=True)

    th12_ufo1 = models.IntegerField(blank=True, null=True)

    th12_ufo2 = models.IntegerField(blank=True, null=True)

    th12_ufo3 = models.IntegerField(blank=True, null=True)

    th125_freeze_area = models.IntegerField(blank=True, null=True)

    extends = models.IntegerField(blank=True, null=True)

    th13_trance = models.IntegerField(blank=True, null=True)

    th14_poc_count = models.IntegerField(blank=True, null=True)

    th14_miss_count = models.IntegerField(blank=True, null=True)

    th16_season = models.IntegerField(blank=True, null=True)

    th17_hyper_fill = models.IntegerField(blank=True, null=True)

    th17_token1 = models.IntegerField(blank=True, null=True)

    th17_token2 = models.IntegerField(blank=True, null=True)

    th17_token3 = models.IntegerField(blank=True, null=True)

    th17_token4 = models.IntegerField(blank=True, null=True)

    th17_token5 = models.IntegerField(blank=True, null=True)



class ReplayFile(models.Model):
    """Represents a replay file or video for a given submission."""

    replay = models.OneToOneField('Replay', on_delete=models.CASCADE)
    """The submission to which this replay corresponds."""

    replay_file = models.BinaryField(max_length=limits.MAX_REPLAY_SIZE, blank=True, null=True)
    """The replay file itself."""

    is_good = models.BooleanField()
    """Whether a replay file can be used unmodified to watch the replay.
    
    Even a desynced replay file can be useful to have. For example, maybe the
    Touhou community will later discover how to fix a certain type of desync.
    """

    video_link = models.TextField(max_length=1000, blank=True, null=True)
    """A URL to a video site with a recording of the run."""


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
