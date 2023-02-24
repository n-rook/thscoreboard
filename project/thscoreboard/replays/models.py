"""Contains all of the models for the replay site."""


import datetime
from typing import Optional

from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.utils.translation import pgettext_lazy

from replays import game_ids
from replays import limits
from replays import replay_parsing
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

    TAS = 2, pgettext_lazy('Category', 'Tool-Assisted')
    """A tool-assisted replay."""

    UNUSUAL = 3, pgettext_lazy('Category', 'Unusual')
    """A special replay that isn't listed on the leaderboards.

    This category is for things like replays of modded games or high-FPS runs;
    replays that don't fall under the TAS category.
    """

    PRIVATE = 4, pgettext_lazy('Category', 'Private')
    """A private replay that isn't shown to anyone.

    Private is deprecated; it will be removed soon. (It does not make sense as a category,
    since a private replay could be REGULAR, TAS or UNUSUAL.)
    """


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


class ReplayQuerySet(models.QuerySet):

    def visible_to(self, viewer: Optional[auth.get_user_model()]) -> 'ReplayQuerySet':
        """Filter out replays that should not be visible to someone.

        This method is closely related to the IsVisible() method on individual replays, but changes the query
        itself instead. As such, it mostly should be preferred to that method, since the unwanted replays are
        not even returned.
        """

        q = self.filter(user__is_active=True)
        if viewer and viewer.is_authenticated:
            q = q.filter(~models.Q(category=Category.PRIVATE) | models.Q(user=viewer))
        else:
            q = q.exclude(category=Category.PRIVATE)
        return q


class Replay(models.Model):
    """Represents a score recorded on the scoreboard."""

    objects = ReplayQuerySet.as_manager()

    class Meta:
        ordering = ['shot', 'difficulty', '-score']

        constraints = [
            models.CheckConstraint(
                check=models.Q(difficulty__gte=0),
                name='difficulty_gte_0'
            ),
            models.CheckConstraint(
                name='replay_type_spell_card_id_isnull',
                check=(
                    models.Q(
                        replay_type=ReplayType.REGULAR,
                        spell_card_id__isnull=True
                    ) | models.Q(
                        replay_type=ReplayType.STAGE_PRACTICE,
                        spell_card_id__isnull=True
                    ) | models.Q(
                        replay_type=ReplayType.SPELL_PRACTICE,
                        spell_card_id__isnull=False
                    ) | models.Q(
                        replay_type=ReplayType.PVP,
                        spell_card_id__isnull=True
                    )
                )
            )
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
    """Timestamp from the replay.

    Timestamps are stored in UTC. However, this may not actually reflect the
    timestamp stored in the replay file.
    """

    name = models.TextField(max_length=12, blank=True, null=True)
    """Username stored in the replay

    The game only allows 8 characters to be added,
    but technically there are 12 bytes allocated, so space is reserved just in case
    """

    slowdown = models.FloatField(blank=True, null=True)
    """Slowdown percentage in the replay

    Should range from 0 to 100, unless ZUN decides otherwise.
    """

    spell_card_id = models.IntegerField(blank=True, null=True)
    """In the case of a spell practice replay, the spell card ID attempted"""

    replay_type = models.IntegerField(choices=ReplayType.choices)
    """Type of replay (regular run, stage practice, etc)"""

    @property
    def lesanae(self):
        """An easter egg."""
        return self.shot.shot_id == 'Sanae' and self.shot.game.game_id == game_ids.GameIDs.TH13

    def IsVisible(self, viewer: auth.get_user_model()):
        """Returns whether this replay should be visible to this user."""

        if not self.user.is_active:
            return False

        if self.category != Category.PRIVATE:
            return True
        return self.user == viewer
    
    def GetNiceFilename(self, id: Optional[int]):
        """Returns a nice filename for this replay.

        This always returns something, even if this submission does not actually
        have a replay file.
        """

        gamecode = game_ids.GetRpyGameCode(self.shot.game.game_id)
        rpy_id = game_ids.MakeBase36ReplayId(self.id if id is None else id)

        return f'{gamecode}_ud{rpy_id}.rpy'

    def SetFromReplayInfo(self, r: replay_parsing.ReplayInfo):
        """Set certain derived fields on this replay from parsed information.

        Note that this function does not affect foreign key fields, such as shot or route.
        """

        self.rep_score = r.score
        self.timestamp = r.timestamp
        self.name = r.name
        self.spell_card_id = r.spell_card_id
        self.replay_type = r.replay_type
        self.slowdown = r.slowdown


class ReplayStage(models.Model):
    """ Represents the end-of-stage data for a stage split for a given replay
        The data may not directly correspond to how it is stored in-game, since some games store it differently
        Most games store the values from the start of the stage
        TH07 stores the values from the end of the stage
        TH08 is weird in that the score is stored from end of stage, but everything else is from the start
    """

    class Meta:
        constraints = [models.UniqueConstraint(fields=['replay', 'stage'], name='unique_stage_per_game')]
        indexes = [models.Index(name='replay_and_stage', fields=['replay', 'stage'])]
        ordering = ['replay', 'stage']

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

    score = models.BigIntegerField(blank=True, null=True)
    """ The current score stored at this stage
        This should be set for all stages that we have data for, but some games do not store end-of-stage data"""

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

    th13_trance = models.IntegerField(blank=True, null=True)
    """Trance gauge value at the stage split in TH13
    This value ranges from 0 to 600, with 1 ingame trance level equalling 200 points
    """

    extends = models.IntegerField(blank=True, null=True)
    """Number of extends (1ups) this run has gotten so far
    More testing needs to be done to find the exact nature of this value,
    whether 1up items affect it or if its just score/life piece extends
    But it's in the data so I will include it

    This value first appears in TH13, but it is present in many modern games so I've
    opted not to specify a game for its name
    """

    th16_season_power = models.IntegerField(blank=True, null=True)
    """Value of the season gauge in TH16"""

    def SetFromReplayStageInfo(self, s: replay_parsing.ReplayStage):
        """Set derived fields on this row from a replay stage.

        Be aware that s.stage must match the current stage of this model
        instance. It is not practical to update the index of a row (since the
        index is part of a unique constraint, so changing it could easily make
        this instance collide with another.)

        Note: In order to avoid unnecessary database calls, for PoFV shots
        the p2 shot type is not updated here.

        Raises:
            ValueError: If this instance's stage index does not match the
                index of the stage passed in.
        """

        if self.stage != s.stage:
            raise ValueError('Stage does not match (old {}, new {})'.format(
                self.stage, s.stage
            ))

        self.stage = s.stage
        self.score = s.score
        self.piv = s.piv
        self.graze = s.graze
        self.point_items = s.point_items
        self.power = s.power
        self.lives = s.lives
        self.life_pieces = s.life_pieces
        self.bombs = s.bombs
        self.bomb_pieces = s.bomb_pieces
        self.th06_rank = s.th06_rank
        self.th07_cherry = s.th07_cherry
        self.th07_cherrymax = s.th07_cherrymax
        self.th09_p1_cpu = s.th09_p1_cpu
        self.th09_p2_cpu = s.th09_p2_cpu
        self.th09_p2_score = s.th09_p2_score
        self.extends = s.extends
        self.th13_trance = s.th13_trance
        self.th16_season_power = s.th16_season_power


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
