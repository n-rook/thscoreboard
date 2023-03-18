import dataclasses
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
    class Meta:
        ordering = ['game_id']

    # A unique ID for the game. For example, th06.
    game_id = models.TextField(primary_key=True)

    # Whether the game supports replay files
    has_replays = models.BooleanField()
    num_difficulties = models.IntegerField()

    def GetName(self):
        return game_ids.GetGameName(self.game_id)

    def GetShortName(self):
        return game_ids.GetGameName(self.game_id, short=True)

    def GetDifficultyName(self, difficulty: int) -> str:
        return game_ids.GetDifficultyName(self.game_id, difficulty)


class Shot(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint('shot_id', 'game', name='unique_shot_per_game')]

    # A unique ID for the shot. For example, ReimuB.
    shot_id = models.TextField()
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    def GetName(self):
        """Get a pretty name for this shot type. Note: Populates game."""
        return game_ids.GetShotName(self.game.game_id, self.shot_id)


class Category(models.IntegerChoices):
    REGULAR = 1, pgettext_lazy('Category', 'Regular')
    TAS = 2, pgettext_lazy('Category', 'Tool-Assisted')
    
    # This category is for things like replays of modded games or high-FPS runs;
    # replays that don't fall under the TAS category.
    UNUSUAL = 3, pgettext_lazy('Category', 'Unusual')
    PRIVATE = 4, pgettext_lazy('Category', 'Private')


class ReplayType(models.IntegerChoices):
    REGULAR = 1, pgettext_lazy('Replay Type', 'Regular')
    STAGE_PRACTICE = 2, pgettext_lazy('Replay Type', 'Stage Practice')
    SPELL_PRACTICE = 3, pgettext_lazy('Replay Type', 'Spell Practice')
    PVP = 4, pgettext_lazy('Replay Type', 'PVP')


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
    route_id = models.TextField()
    order_number = models.IntegerField()
    """A number used only to order the routes in a game.

    For example, if two routes have 1 and 2, the route with 1 is listed first,
    then the route with 2.
    """

    def GetName(self):
        return game_ids.GetRouteName(self.game.game_id, self.route_id)


class ReplayQuerySet(models.QuerySet):

    def visible_to(self, viewer: Optional[auth.get_user_model()]) -> 'ReplayQuerySet':
        q = self.filter(user__is_active=True)
        if viewer and viewer.is_authenticated:
            q = q.filter(~models.Q(category=Category.PRIVATE) | models.Q(user=viewer))
        else:
            q = q.exclude(category=Category.PRIVATE)
        return q


@dataclasses.dataclass(frozen=True)
class ReplayConstantModels:
    game: Game
    shot: Shot
    route: Optional[Route]


class Replay(models.Model):

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
    category = models.IntegerField(choices=Category.choices)
    created = models.DateTimeField(auto_now_add=True)
    shot = models.ForeignKey('Shot', on_delete=models.PROTECT)
    difficulty = models.IntegerField()
    route = models.ForeignKey('Route', on_delete=models.PROTECT, blank=True, null=True)

    def GetDifficultyName(self):
        return game_ids.GetDifficultyName(self.shot.game.game_id, self.difficulty)

    def GetDifficultyUrlCode(self):
        return f'd{self.difficulty}'

    score = models.BigIntegerField()

    # Whether a replay file can be used unmodified to watch the replay
    is_good = models.BooleanField(blank=True, null=True)
    is_clear = models.BooleanField()
    rep_score = models.BigIntegerField(blank=True, null=True)
    video_link = models.TextField(max_length=1000)
    comment = models.TextField(max_length=limits.MAX_COMMENT_LENGTH)
    timestamp = models.DateTimeField(blank=True, null=True)  # UTC timestamp
    name = models.TextField(max_length=12, blank=True, null=True)
    slowdown = models.FloatField(blank=True, null=True)
    spell_card_id = models.IntegerField(blank=True, null=True)
    replay_type = models.IntegerField(choices=ReplayType.choices)

    @property
    def lesanae(self):
        """An easter egg."""
        return self.shot.shot_id == 'Sanae' and self.shot.game.game_id == game_ids.GameIDs.TH13

    def IsVisible(self, viewer: auth.get_user_model()):
        if not self.user.is_active:
            return False

        if self.category != Category.PRIVATE:
            return True
        return self.user == viewer

    def GetNiceFilename(self, id: Optional[int]) -> str:
        gamecode = game_ids.GetRpyGameCode(self.shot.game.game_id)
        rpy_id = game_ids.MakeBase36ReplayId(self.id if id is None else id)

        return f'{gamecode}_ud{rpy_id}.rpy'

    def SetFromReplayInfo(self, r: replay_parsing.ReplayInfo):
        self.rep_score = r.score
        self.timestamp = r.timestamp
        self.name = r.name
        self.spell_card_id = r.spell_card_id
        self.replay_type = r.replay_type
        self.slowdown = r.slowdown

    def SetForeignKeysFromConstantModels(self, c: ReplayConstantModels):
        self.shot = c.shot
        self.route = c.route


class ReplayStage(models.Model):

    class Meta:
        constraints = [models.UniqueConstraint(fields=['replay', 'stage'], name='unique_stage_per_game')]
        indexes = [models.Index(name='replay_and_stage', fields=['replay', 'stage'])]
        ordering = ['replay', 'stage']

    replay = models.ForeignKey('Replay', on_delete=models.CASCADE)
    stage = models.IntegerField()
    score = models.BigIntegerField(blank=True, null=True)
    piv = models.IntegerField(blank=True, null=True)
    graze = models.IntegerField(blank=True, null=True)
    point_items = models.IntegerField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    lives = models.IntegerField(blank=True, null=True)
    life_pieces = models.IntegerField(blank=True, null=True)
    bombs = models.IntegerField(blank=True, null=True)
    bomb_pieces = models.IntegerField(blank=True, null=True)
    th06_rank = models.IntegerField(blank=True, null=True)
    th07_cherry = models.IntegerField(blank=True, null=True)
    th07_cherrymax = models.IntegerField(blank=True, null=True)
    th09_p1_cpu = models.BooleanField(blank=True, null=True)
    th09_p2_cpu = models.BooleanField(blank=True, null=True)
    th09_p2_shot = models.ForeignKey('Shot', on_delete=models.PROTECT, blank=True, null=True)
    th09_p2_score = models.IntegerField(blank=True, null=True)
    th13_trance = models.IntegerField(blank=True, null=True)
    
    # More testing needs to be done to find the exact nature of this value,
    # whether 1up items affect it or if its just score/life piece extends
    extends = models.IntegerField(blank=True, null=True)
    th16_season_power = models.IntegerField(blank=True, null=True)

    def SetFromReplayStageInfo(self, s: replay_parsing.ReplayStage):
        
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

    class Meta:
        constraints = [models.UniqueConstraint(fields=['replay_hash'], name='unique_hash')]

    replay = models.OneToOneField('Replay', on_delete=models.CASCADE)
    replay_file = models.BinaryField(max_length=limits.MAX_REPLAY_SIZE, blank=True, null=True)

    # A SHA-256 hash of the replay file
    replay_hash = models.BinaryField(max_length=32)


class TemporaryReplayFile(models.Model):
    """Represents a temporarily held replay file a user is uploading.

    When the user is uploading a replay file, we want the server to receive the
    file and parse metadata from it to help the user. However, this means that the
    replay must be saved before it is published.
    """

    TTL = datetime.timedelta(days=30)

    @classmethod
    def CleanUp(cls, now: datetime.datetime) -> None:
        """Delete old temporary replay files."""
        return model_ttl.CleanUpOldRows(cls, now)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    replay = models.BinaryField(max_length=limits.MAX_REPLAY_SIZE)
