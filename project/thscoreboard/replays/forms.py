"""Various forms useful for the replays site."""

from typing import Any, List, Sequence, Tuple
from urllib import parse

from django import forms
from django.core import exceptions
from django.db.models import enums

from replays.get_all_games import get_pc98_games, get_windows_games
from replays import game_ids
from replays import game_fields
from replays import models
from replays import limits
from replays.lib import custom_fields

difficulty_names = (
    ("0", "Easy"),
    ("1", "Normal"),
    ("2", "Hard"),
    ("3", "Lunatic"),
    ("4", "Extra"),
    ("5", "Phantasm"),
)


class UnboundFormError(Exception):
    """A form was unbound, but this operation requires it be bound."""


_ALLOWED_REPLAY_HOSTS = [
    "www.youtube.com",
    "youtu.be",
    "www.twitch.tv",
    "www.bilibili.com",
]


def _AllowedVideoDomainsValidator(value: str):
    split_url = parse.urlsplit(value)
    if split_url.hostname not in _ALLOWED_REPLAY_HOSTS:
        raise exceptions.ValidationError(
            "If present, the replay link must be to one of the following sites: %(sites_comma_separated)s",
            params={"sites_comma_separated": ", ".join(_ALLOWED_REPLAY_HOSTS)},
        )
    elif split_url.hostname == "www.youtube.com" and split_url.path.startswith(
        "/embed/"
    ):
        raise exceptions.ValidationError("The replay link cannot be an embed link")


def _GetDifficultyChoices(game: models.Game) -> Tuple[int, str]:
    """Return pairs like (0, "Easy") for each difficulty of a game."""
    return [
        (i, game_ids.GetDifficultyName(game.game_id, i))
        for i in range(game.num_difficulties)
    ]


def _create_comment_field():
    return forms.CharField(
        max_length=limits.MAX_COMMENT_LENGTH, required=False, widget=forms.Textarea
    )


def _get_replay_type_choices(game: models.Game) -> list[Tuple[str, str]]:
    replay_types = [models.ReplayType.FULL_GAME, models.ReplayType.STAGE_PRACTICE]
    if game_fields.game_has_pvp(game.game_id):
        replay_types.append(models.ReplayType.PVP)
    return _enum_to_form_choices(replay_types)


def _enum_to_form_choices(
    enum_choices: Sequence[enums.Choices],
) -> List[Tuple[Any, str]]:
    """Convert Django model enum list to a form choice list."""
    return [(v, v.label) for v in enum_choices]


class ShotField(forms.ModelChoiceField):
    """A field defining shot type. You must call set_queryset before using."""

    def __init__(self):
        super().__init__(
            queryset=None,
            empty_label=None,
        )

    @classmethod
    def set_queryset(self, field: "ShotField", game_id: str):
        field.queryset = models.Shot.objects.filter(game=game_id)

    def label_from_instance(self, obj: models.Shot) -> str:
        return obj.GetName()


class RouteField(forms.ModelChoiceField):
    """A field defining route type. You must call set_queryset before using."""

    def __init__(self):
        super().__init__(queryset=None, empty_label=None)

    @classmethod
    def set_queryset(self, field: "RouteField", game_id: str):
        field.queryset = models.Route.objects.filter(game=game_id)

    def label_from_instance(self, obj: models.Route) -> str:
        return obj.GetName()

    def should_include(self) -> bool:
        """Whether or not the Route field should be included in the form.

        Most Touhou games don't have routes, so they don't need this field.
        """
        return self.choices


class VideoReplayLinkField(forms.URLField):
    default_validators = forms.URLField.default_validators + [
        _AllowedVideoDomainsValidator
    ]


# TODO: Fix up so that these settings are set dynamically based on game


class UploadReplayFileForm(forms.Form):
    replay_file = forms.FileField()


def initialize_publish_replay_form_from_replay(
    r: models.Replay, data=None
) -> "PublishReplayForm":
    """Return a new PublishReplayForm based on an existing replay.

    Information from the Replay is used to populate the "initial" data. Note
    that initial data is not used as a fallback for real values from a
    populated form. See
    https://docs.djangoproject.com/en/4.2/ref/forms/fields/#initial for more
    detail.

    Args:
        r: The replay to use as initial values.
        data: If present, form data from a POST used to populate the Form.

    Returns:
        A PublishReplayForm.
    """

    return PublishReplayForm(
        r.shot.game.game_id,
        r.replay_type,
        initial={
            "name": r.name,
            "score": r.score,
            "category": r.category,
            "comment": r.comment,
            "is_good": r.is_good,
            "is_clear": r.is_clear,
            "video_link": r.video_link,
            "uses_bombs": not r.no_bomb,
            "misses": r.miss_count,
        },
        data=data,
    )


class PublishReplayForm(forms.Form):
    def __init__(self, gameID: str, replay_type: models.ReplayType, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"readonly": "readonly"})
        #   i don't like using the negative here but it kind of has to be
        if gameID not in [game_ids.GameIDs.TH09]:
            self.fields["score"].widget.attrs.update({"readonly": "readonly"})

        if not game_ids.HasBombs(gameID, replay_type=replay_type):
            del self.fields["uses_bombs"]
        if not game_ids.HasLives(gameID, replay_type=replay_type):
            del self.fields["misses"]

    score = forms.IntegerField(min_value=0)
    category = custom_fields.ChoicesEnumField(models.Category)
    comment = _create_comment_field()
    is_good = forms.BooleanField(initial=True, required=False)
    is_clear = forms.BooleanField(initial=True, required=False)
    video_link = VideoReplayLinkField(required=False)
    name = forms.CharField(max_length=12, required=False)

    uses_bombs = forms.BooleanField(initial=True, required=False)
    misses = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data["is_good"] and not cleaned_data["video_link"]:
            self.add_error(
                "video_link",
                exceptions.ValidationError(
                    "If your replay desyncs, please provide a video "
                    "so it can still be watched."
                ),
            )

    def update_replay(self, r: models.Replay):
        """Update an existing Replay row with information from this form.

        This form must be bound and cleaned. This method does not save
        the updated replay.

        Args:
            r: The replay to update.
        """
        if not self.is_bound:
            raise UnboundFormError()

        r.score = self.cleaned_data["score"]
        r.category = self.cleaned_data["category"]
        r.comment = self.cleaned_data["comment"]
        r.is_good = self.cleaned_data["is_good"]
        r.is_clear = self.cleaned_data["is_clear"]
        if "uses_bombs" in self.cleaned_data:
            r.no_bomb = not self.cleaned_data["uses_bombs"]
        else:
            r.no_bomb = None
        if "misses" in self.cleaned_data:
            r.miss_count = self.cleaned_data["misses"]
        else:
            r.miss_count = None
        r.video_link = self.cleaned_data["video_link"]


class PublishReplayWithoutFileForm(forms.Form):
    def __init__(self, *args, game: models.Game, **kwargs):
        super().__init__(*args, **kwargs)

        ShotField.set_queryset(self.fields["shot"], game.game_id)
        RouteField.set_queryset(self.fields["route"], game.game_id)

        if not self.fields["route"].should_include():
            del self.fields["route"]

        self.fields["difficulty"].choices = _GetDifficultyChoices(game)
        self.fields["replay_type"].choices = _get_replay_type_choices(game)

        if not game_ids.HasBombs(game.game_id):
            del self.fields["uses_bombs"]
        if not game_ids.HasLives(game.game_id):
            del self.fields["misses"]

    difficulty = forms.ChoiceField(choices=difficulty_names, initial=1)
    shot = ShotField()
    route = RouteField()
    score = forms.IntegerField(min_value=0)
    category = custom_fields.ChoicesEnumField(models.Category)
    replay_type = custom_fields.ChoicesEnumField(models.ReplayType)  # overridden
    is_clear = forms.BooleanField(initial=True, required=False)
    comment = _create_comment_field()
    video_link = VideoReplayLinkField(required=True)

    uses_bombs = forms.BooleanField(initial=True, required=False)
    misses = forms.IntegerField(required=False)


class EditReplayForm(forms.Form):
    comment = _create_comment_field()


class RankingGameSelectionForm(forms.Form):
    SELECT_ALL = "All games"
    SELECT_PC98 = "PC-98"
    SELECT_WINDOWS = "Windows"
    GROUPED_SELECTIONS = [SELECT_ALL, SELECT_PC98, SELECT_WINDOWS]
    DEFAULT_SELECTION = SELECT_WINDOWS

    grouped_game_selection = forms.ChoiceField(
        choices=[(g, g) for g in GROUPED_SELECTIONS], required=False
    )
    pc98_game_selection = forms.ChoiceField(required=False)
    windows_game_selection = forms.ChoiceField(required=False)

    def get_selection(self) -> str:
        return (
            self.cleaned_data["grouped_game_selection"]
            or self.cleaned_data["pc98_game_selection"]
            or self.cleaned_data["windows_game_selection"]
            or self.DEFAULT_SELECTION
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pc98_game_selection"].choices = [
            (c.game_id, c.GetShortName()) for c in get_pc98_games()
        ]
        self.fields["windows_game_selection"].choices = [
            (c.game_id, c.GetShortName()) for c in get_windows_games()
        ]

        self.all_choice_fields = [
            ("grouped_game_selection", self.fields["grouped_game_selection"]),
            ("pc98_game_selection", self.fields["pc98_game_selection"]),
            ("windows_game_selection", self.fields["windows_game_selection"]),
        ]
