"""Contains all of the models for the replay site."""


import datetime

from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.utils.translation import pgettext_lazy

from replays import game_ids
from replays import limits
from shared_content import model_ttl
from thscoreboard import settings


class Game(models.Model):
    """Represents a single Touhou game."""

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

    def GetDifficultyName(self, difficulty: int) -> str:
        """Gets the name of a difficulty in this game."""
        return game_ids.GetDifficultyName(self.game_id, difficulty)


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
    """The category under which a replay is uploaded."""

    REGULAR = 1, pgettext_lazy('Category', 'Regular')
    """A normal upload; a legitimate replay played by a real player."""

    TAS = 2, pgettext_lazy('Category', 'TAS')
    """A tool-assisted replay."""

    UNUSUAL = 3, pgettext_lazy('Category', 'Unusual')
    """A special replay that isn't listed on the leaderboards.

    This category is for things like replays of modded games or high-FPS runs;
    replays that don't fall under the TAS category.
    """

    PRIVATE = 4, pgettext_lazy('Category', 'Private')
    """A private replay that isn't shown to anyone."""


class ReplayType(models.IntegerChoices):
    """Type of replay (regular, spell practice, etc)"""

    REGULAR = 1, pgettext_lazy('Replay Type', 'Regular')
    """A regular 1cc/scoring run"""

    STAGE_PRACTICE = 2, pgettext_lazy('Replay Type', 'Stage Practice')
    """Stage practice replay. Note: a regular replay that gameovers at stage 1 will be detected as a stage practice replay"""

    SPELL_PRACTICE = 3, pgettext_lazy('Replay Type', 'Spell Practice')
    """A spell practice replay. Note: stage practice replays that start at a spell using THPRAC will be detected as stage practice
        This is only for replays using the ingame spell practice option"""

    PVP = 4, pgettext_lazy('Replay Type', 'PVP')
    """Player vs player replays"""


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


class Replay(models.Model):
    """Represents a score recorded on the scoreboard."""

    class Meta:
        ordering = ['shot', 'difficulty', '-score']

        constraints = [
            models.CheckConstraint(
                check=models.Q(difficulty__gte=0),
                name='difficulty_gte_0'
            ),
        ]

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

    score = models.BigIntegerField()
    """The score of the replay."""

    is_good = models.BooleanField(blank=True, null=True)
    """Whether a replay file can be used unmodified to watch the replay.

    Even a desynced replay file can be useful to have. For example, maybe the
    Touhou community will later discover how to fix a certain type of desync.

    If this submission has no replay file, this field will be null.
    """

    is_clear = models.BooleanField()
    """Whether the replay cleared the game."""

    rep_score = models.BigIntegerField(blank=True, null=True)
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

    name = models.TextField(max_length=12, blank=True, null=True)
    """Username stored in the replay

    The game only allows 8 characters to be added,
    but technically there are 12 bytes allocated, so space is reserved just in case
    """

    spell_card_id = models.IntegerField(blank=True, null=True)
    """In the case of a spell practice replay, the spell card ID attempted"""

    replay_type = models.IntegerField(choices=ReplayType.choices)
    """Type of replay (regular run, stage practice, etc)"""

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
        gamecode = self.shot.game.game_id

        if ascii_only:
            return '{gamecode}_{id}.rpy'.format(
                gamecode=gamecode,
                id=self.id
            )
        else:
            return '{gamecode}_{user}_{id}.rpy'.format(
                gamecode=gamecode,
                user=self.user.username,
                id=self.id,
            )


class ReplayStage(models.Model):
    """ Represents a stage split for a given replay
        Most games store the values from the start of the stage
        TH07 stores the values from the end of the stage
        TH08 is weird in that the score is stored from end of stage, but everything else is from the start
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

    th07_cherry = models.IntegerField(blank=True, null=True)
    """Current cherry value for TH07"""

    th07_cherrymax = models.IntegerField(blank=True, null=True)
    """Current cherry max for TH07"""

    th09_p1_cpu = models.BooleanField(blank=True, null=True)
    """Whether player 1 in the stage split is a CPU or not in TH09"""

    th09_p2_cpu = models.BooleanField(blank=True, null=True)
    """Whether player 2 in the stage split is a CPU or not in TH09"""

    th09_p2_shot = models.ForeignKey('Shot', on_delete=models.PROTECT, blank=True, null=True)
    """The shot type stored for player 2 in the stage split in TH09"""

    th09_p2_score = models.IntegerField(blank=True, null=True)
    """The score stored for player 2 in the stage split in TH09"""


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

    TTL = datetime.timedelta(days=30)

    @classmethod
    def CleanUp(cls, now: datetime.datetime) -> None:
        """Delete old temporary replay files.

        Args:
            now: The current time.

        Returns:
            The number of deleted files.
        """
        return model_ttl.CleanUpOldRows(cls, now)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    """The user who uploaded the temporary replay."""

    created = models.DateTimeField(default=timezone.now)
    """When the replay file was uploaded."""

    replay = models.BinaryField(max_length=limits.MAX_REPLAY_SIZE)
    """The replay file itself."""
