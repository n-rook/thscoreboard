"""Contains all of the models for the replay site."""

import dataclasses
import datetime
from typing import Optional

from django.db import models
from django.db import utils
from django.utils import formats
from django.utils import timezone
from django.utils.translation import pgettext_lazy
from django.db.models import Q, F, Window, QuerySet, When, Case, Value
from django.db.models.functions import RowNumber

from replays import game_ids
from replays import limits
from replays import replay_parsing
from shared_content import db_errors
from shared_content import model_ttl
from thscoreboard import settings


class Game(models.Model):
    """Represents a single Touhou game."""

    class Meta:
        ordering = ["game_id"]

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
        """Get a standard name for the game."""
        return game_ids.GetGameName(self.game_id, game_ids.NameLength.STANDARD)

    def GetShortName(self):
        """Get a short name for this game, suitable for a column in a table."""
        return game_ids.GetGameName(self.game_id, game_ids.NameLength.SHORT)

    def GetFullName(self):
        """Get the full name for this game."""
        return game_ids.GetGameName(self.game_id, game_ids.NameLength.FULL)

    def GetDifficultyName(self, difficulty: int) -> str:
        """Gets the name of a difficulty in this game."""
        return game_ids.GetDifficultyName(self.game_id, difficulty)

    def GetIconPath(self) -> str:
        """Get the HTTP path to get a small icon for this game."""
        return f"/static/icons/{self.game_id}.png"


class Shot(models.Model):
    """The character selected by the player.

    If a game has both "shots" and "subshots", this includes both. For example,
    in EoSD, Reimu has two Shot rows, "ReimuA" and "ReimuB".

    All games have shots. (This makes a lot of code simpler, since it can
    assume the presence of a shot type.) If a game does not let the player
    select a shot, a single row is defined, named after the protagonist.
    """

    class Meta:
        constraints = [
            models.UniqueConstraint("shot_id", "game", name="unique_shot_per_game")
        ]

    shot_id = models.TextField()
    """A unique ID for the shot.

    Typically, this is the name of the character (in English), plus perhaps a
    letter. For example, Touhou 6 contains "ReimuA", "ReimuB", "MarisaA" and
    "MarisaB".
    """

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    """The game in which this shot appears."""

    def GetName(self):
        """Get a pretty name for this shot type. Note: Populates game."""
        return game_ids.GetShotName(self.game.game_id, self.shot_id)

    def GetCharacterName(self) -> str:
        """Get a pretty name for this Character. Note: Populates game."""
        return game_ids.GetCharacterName(self.game.game_id, self.shot_id)

    def GetSubshotName(self) -> str:
        """Get a pretty name for this subshot. Note: Populates game."""
        return game_ids.GetSubshotName(self.game.game_id, self.shot_id)


class Category(models.IntegerChoices):
    """The category under which a replay is uploaded."""

    STANDARD = 1, pgettext_lazy("Category", "Standard")
    """A normal upload; a legitimate replay played by a real player."""

    TAS = 2, pgettext_lazy("Category", "Tool-Assisted")
    """A tool-assisted replay."""

    UNUSUAL = 3, pgettext_lazy("Category", "Unusual")
    """A special replay that isn't listed on the leaderboards.

    This category is for things like replays of modded games or high-FPS runs;
    replays that don't fall under the TAS category.
    """


class ReplayType(models.IntegerChoices):
    """Type of replay (full game, spell practice, etc)"""

    FULL_GAME = 1, pgettext_lazy("Replay Type", "Full Game")
    """A run of the whole game."""

    STAGE_PRACTICE = 2, pgettext_lazy("Replay Type", "Stage Practice")
    """A replay of stage practice.

    Known bug: A full game replay that ends in Stage 1 may be detected as stage practice.
    """

    SPELL_PRACTICE = 3, pgettext_lazy("Replay Type", "Spell Practice")
    """A spell practice replay. Note: stage practice replays that start at a spell using THPRAC will be detected as stage practice
        This is only for replays using the ingame spell practice option"""

    PVP = 4, pgettext_lazy("Replay Type", "PVP")
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
        constraints = [
            models.UniqueConstraint("route_id", "game", name="unique_route_per_game")
        ]

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
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


@dataclasses.dataclass(frozen=True)
class ReplayConstantModels:
    game: Game
    shot: Shot
    route: Optional[Route]


class ReplayQuerySet(QuerySet):
    def filter_visible(self) -> "ReplayQuerySet":
        """Filter out replays that should not be visible.

        This method is closely related to the IsVisible() method on individual replays, but changes the query
        itself instead. As such, it mostly should be preferred to that method, since the unwanted replays are
        not even returned.
        """

        return self.filter(Q(user__is_active=True) | Q(imported_username__isnull=False))

    def annotate_with_rank(self) -> "ReplayQuerySet":
        """Annotate each standard replay with a rank, starting from 1 descending, with
        separate ranks for each difficulty and shot. Set rank to -1 for other replays.
        """

        return self.annotate(
            rank=Case(
                When(
                    Q(category=Category.STANDARD) & Q(replay_type=ReplayType.FULL_GAME),
                    then=Window(
                        expression=RowNumber(),
                        order_by=[
                            F("score").desc(),
                            F("created"),
                            F("id"),
                        ],
                        partition_by=[
                            F("shot_id"),
                            F("difficulty"),
                            F("shot__game_id"),
                            F("route"),
                        ],
                    ),
                ),
                default=Value(-1),
                output_field=models.IntegerField(),
            )
        )

    def ghosts_of(self, replay_hash: bytes) -> "ReplayQuerySet":
        """Matches ghosts of a given replay file.

        A "ghost" of a replay is an existing replay with an identical ReplayFile
        assigned to an inactive user account. Such replays exist in the database so
        they can be brought back to life if the user account is revived. However, to
        users they do not exist, so it is inappropriate to prevent users from uploading
        duplicates of ghosts.
        """
        return self.filter(
            replayfile__replay_hash=replay_hash,
            user__is_active=False,
        )


class Replay(models.Model):
    """Represents a score recorded on the scoreboard."""

    objects = ReplayQuerySet().as_manager()

    class Meta:
        ordering = ["shot", "difficulty", "-score"]

        constraints = [
            models.CheckConstraint(
                check=models.Q(difficulty__gte=0), name="difficulty_gte_0"
            ),
            models.CheckConstraint(
                name="replay_type_spell_card_id_isnull",
                check=(
                    models.Q(
                        replay_type=ReplayType.FULL_GAME, spell_card_id__isnull=True
                    )
                    | models.Q(
                        replay_type=ReplayType.STAGE_PRACTICE,
                        spell_card_id__isnull=True,
                    )
                    | models.Q(
                        replay_type=ReplayType.SPELL_PRACTICE,
                        spell_card_id__isnull=False,
                    )
                    | models.Q(replay_type=ReplayType.PVP, spell_card_id__isnull=True)
                ),
            ),
            models.CheckConstraint(
                name="user_or_imported_username_is_nonnull",
                check=models.Q(user__isnull=False)
                | models.Q(imported_username__isnull=False),
            ),
        ]

        indexes = [
            # Supports querying for the top scores in some field.
            models.Index(
                name="scoring_division",
                fields=[
                    "replay_type",
                    "shot_id",
                    "difficulty",
                    "route_id",
                    "category",
                    "-score",
                ],
            )
        ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    """The user who uploaded the replay."""

    imported_username = models.TextField(max_length=12, blank=True, null=True)
    """The user who uploaded the replay to an extrenal site, such as royalflare."""

    category = models.IntegerField(choices=Category.choices)

    created = models.DateTimeField(default=datetime.datetime.now)
    """When the replay was uploaded."""

    shot = models.ForeignKey("Shot", on_delete=models.PROTECT)
    """The shot type the player used."""

    difficulty = models.IntegerField()
    """The difficulty on which the player played."""

    route = models.ForeignKey("Route", on_delete=models.PROTECT, blank=True, null=True)
    """The route on which the game was played."""

    def GetDifficultyName(self):
        """Get a pretty name for this difficulty. Note: Populates shot and game."""
        return game_ids.GetDifficultyName(self.shot.game.game_id, self.difficulty)

    def GetDifficultyUrlCode(self):
        return f"d{self.difficulty}"

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
    """Type of replay (full run run, stage practice, etc)"""

    def GetReplayTypeName(self) -> str:
        """Returns a string description of this replay's type."""
        return game_ids.GetReplayType(self.replay_type)

    no_bomb = models.BooleanField(blank=True, null=True)
    """Whether the replay uses no bombs (a popular challenge condition).

    If null, one of these two things is the case:
    - NB doesn't make sense for the game, because it has no bombs (like PoFV)
    - This is an old replay, and we don't know if it used bombs or not.

    You may ask, "why is this 'no_bomb' and not 'used_bombs'"? Two reasons: First,
    Touhou players tend to think about 'no_bomb' as a positive trait, despite
    the name. Second, it means that we can call a replay no_bomb if bool(no_bomb)
    is True (collapsing False and None into one value).
    """

    miss_count = models.IntegerField(blank=True, null=True)
    """The number of times the player died during the run.

    This field is optional; if it is null, the player probably just didn't set it.
    """

    is_listed = models.BooleanField(default=True)
    """Whether the replay is listed on the leaderboards. Unlisted replays are still
    shown on a user's profile.
    """

    @property
    def lesanae(self):
        """An easter egg."""
        return (
            self.shot.shot_id == "Sanae"
            and self.shot.game.game_id == game_ids.GameIDs.TH13
        )

    def IsVisible(self):
        """Returns whether this replay should be publicly visible."""
        return self.imported_username is not None or self.user.is_active

    def GetNiceFilename(self, id: Optional[int]):
        """Returns a nice filename for this replay.

        This always returns something, even if this submission does not actually
        have a replay file.
        """

        gamecode = game_ids.GetRpyGameCode(self.shot.game.game_id)
        rpy_id = game_ids.MakeBase36ReplayId(self.id if id is None else id)

        return f"{gamecode}_ud{rpy_id}.rpy"

    def GetRank(self) -> int | None:
        """Returns this replay's rank if it is a top-ranking replay.

        Only the top 3 replays (in a given field: the ranking is divided
        by game, shot, difficulty, and so on) have a rank; for the others,
        None is returned.

        This method is instant if "rank_view" is selected, which is strongly
        recommended.
        """
        if hasattr(self, "rank_view"):
            return self.rank_view.place
        else:
            return None

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

    def SetForeignKeysFromConstantModels(self, c: ReplayConstantModels):
        """Set the shot and route foreign keys on this Replay."""
        self.shot = c.shot
        self.route = c.route

    def GetShortenedComment(self) -> str:
        """Gets a short version of the replay comment, suitable to be displayed
        in a table row."""
        if len(self.comment) <= limits.MAX_SHORTENED_COMMENT_LENGTH:
            return self.comment
        return self.comment[: limits.MAX_SHORTENED_COMMENT_LENGTH] + "..."

    def GetFormattedTimestampDate(self) -> Optional[str]:
        """Returns the date on which the replay was played."""

        if not self.timestamp:
            return None

        if self.shot.game_id == game_ids.GameIDs.TH07:
            fmt = "d F"
        else:
            fmt = "d F Y"

        return formats.date_format(self.timestamp, format=fmt)


class ReplayRank(models.Model):
    """Represents a replay's rank on the scoreboard.

    Most replays are not listed here. Only top-3 replays in a field will have
    rows in this view.

    IMPORTANT NOTE: This model represents a view, not a table. It is defined
    by the following query:

    CREATE OR REPLACE VIEW replays_rank
    AS
    SELECT row_number() over () as id, replay, score, shot_id, difficulty, route_id, category, place
    FROM (
    SELECT id as replay, score, shot_id, difficulty, route_id, category, rank() OVER (PARTITION BY shot_id, difficulty, route_id, category ORDER BY score DESC, created, id) as place
    FROM replays_replay
    WHERE replay_type = 1  -- FULL_GAME
    AND (category = 1 OR category = 2)  -- STANDARD or TAS
    ) AS ranked
    WHERE place <= 3
    ORDER BY shot_id, difficulty, route_id, category, place desc
    ;
    """

    class Meta:
        db_table = "replays_rank"
        managed = False

    replay = models.OneToOneField(
        "Replay",
        db_column="replay",
        on_delete=models.DO_NOTHING,
        related_name="rank_view",
    )
    """The replay being ranked."""

    shot = models.ForeignKey("Shot", on_delete=models.DO_NOTHING)

    difficulty = models.IntegerField()
    """The difficulty on which the player played."""

    route = models.ForeignKey(
        "Route", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    """The route on which the game was played."""

    category = models.IntegerField(choices=Category.choices)

    place = models.IntegerField("Place")
    """The replay's rank. 1 is first place, 2 is second, 3 is third.

    In the case of a tie, the tied replays will all share the same place.
    """


class ReplayStage(models.Model):
    """Represents the end-of-stage data for a stage split for a given replay
    The data may not directly correspond to how it is stored in-game, since some games store it differently
    Many games only store the data from the start of a replay, so many of the fields for the final stage will be null
    """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["replay", "stage"], name="unique_stage_per_game"
            )
        ]
        indexes = [models.Index(name="replay_and_stage", fields=["replay", "stage"])]
        ordering = ["replay", "stage"]

    replay = models.ForeignKey("Replay", on_delete=models.CASCADE)
    """The replay this split corresponds to"""

    stage = models.IntegerField()
    """ The stage this split corresponds to in the replay
        This is 1-indexed, regular stages are numbered in order, typically 1-6, extra is the stage after, usually 7
    """

    score = models.BigIntegerField(blank=True, null=True)
    """ The current score stored at this stage"""

    piv = models.IntegerField(blank=True, null=True)
    """ The current PIV stored at this stage
        This may be named as a different mechanic in some games, but it functions and is stored the same
        The actual value stored in some games might have extra precision, we are only storing the functional amount visible to the player
    """

    graze = models.IntegerField(blank=True, null=True)
    """ The current graze stored at this stage"""

    point_items = models.IntegerField(blank=True, null=True)
    """ The number of point items acquired at this stage"""

    power = models.IntegerField(blank=True, null=True)
    """ The player's power at this stage
        In the modern windows games (TH10 onwards), the displayed power is in a different format to the stored/internal power
    """

    lives = models.IntegerField(blank=True, null=True)
    """ The number of extra lives at this stage"""

    life_pieces = models.IntegerField(blank=True, null=True)
    """ The number of life pieces at this stage"""

    bombs = models.IntegerField(blank=True, null=True)
    """ The number of bombs at this stage"""

    bomb_pieces = models.IntegerField(blank=True, null=True)
    """ The number of bomb pieces at this stage"""

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

    th09_p2_shot = models.ForeignKey(
        "Shot", on_delete=models.PROTECT, blank=True, null=True
    )
    """The shot type stored for player 2 in the stage split in TH09"""

    th09_p2_score = models.IntegerField(blank=True, null=True)
    """The score stored for player 2 in the stage split in TH09"""

    th13_trance = models.IntegerField(blank=True, null=True)
    """Trance gauge value at the stage split in TH13
    This value ranges from 0 to 600, with 1 ingame trance level equalling 200 points
    """

    th128_motivation = models.IntegerField(blank=True, null=True)
    """Motivation percentage, which acts like lives but is different. Stored as a fixed point integer where 10000 is 100%
    The last 2 digits are cut off in the game"""

    th128_perfect_freeze = models.IntegerField(blank=True, null=True)
    """Perfect Freeze percentage. Stored as a fixed point integer where 10000 is 100%
    The last 2 digits are cut off in the game"""

    th128_frozen_area = models.FloatField(blank=True, null=True)
    """Sum of all frozen area percentages so far. Note that 100% is stored as 100, not 1
    Anything beyond the decimal point is cut off in the game"""

    extends = models.IntegerField(blank=True, null=True)
    """Number of extends (1ups) this run has gotten so far
    More testing needs to be done to find the exact nature of this value,
    whether 1up items affect it or if its just score/life piece extends

    This value first appears in TH13 and is used to determine the number of life pieces needed for a 1up
    It is present in many modern games so I've opted not to specify a game for its name
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
            raise ValueError(
                "Stage does not match (old {}, new {})".format(self.stage, s.stage)
            )

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
        self.th128_motivation = s.th128_motivation
        self.th128_perfect_freeze = s.th128_perfect_freeze
        self.th128_frozen_area = s.th128_frozen_area
        self.th13_trance = s.th13_trance
        self.th16_season_power = s.th16_season_power


_REPLAY_FILE_UNIQUE_HASH_CONSTRAINT = "unique_hash"


class ReplayFile(models.Model):
    """Represents a replay file for a given score."""

    @classmethod
    def IsUniqueHashCollisionError(cls, e: utils.IntegrityError):
        return (
            db_errors.IsUniqueError(e)
            and db_errors.GetUniqueConstraintCause(e)
            == _REPLAY_FILE_UNIQUE_HASH_CONSTRAINT
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["replay_hash"], name=_REPLAY_FILE_UNIQUE_HASH_CONSTRAINT
            )
        ]

    replay = models.OneToOneField("Replay", on_delete=models.CASCADE)
    """The submission to which this replay corresponds."""

    replay_file = models.BinaryField(
        max_length=limits.MAX_REPLAY_SIZE, blank=True, null=True
    )
    """The replay file itself."""

    replay_hash = models.BinaryField(max_length=32)
    """A SHA-256 hash of the replay file, to check for duplicates"""


class TemporaryReplayFile(models.Model):
    """Represents a temporarily held replay file a user is uploading.

    When the user is uploading a replay file, we want the server to receive the
    file and parse metadata from it to help the user. However, this means that the
    replay must be saved before it is published.
    """

    TTL = datetime.timedelta(days=30)

    @classmethod
    def CleanUp(cls, now: datetime.datetime) -> None:
        """Delete old temporary replay files"""
        return model_ttl.CleanUpOldRows(cls, now)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    """The user who uploaded the temporary replay."""

    created = models.DateTimeField(default=timezone.now)
    """When the replay file was uploaded."""

    replay = models.BinaryField(max_length=limits.MAX_REPLAY_SIZE)
    """The replay file itself."""
