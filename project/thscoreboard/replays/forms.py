"""Various forms useful for the replays site."""

from typing import Tuple
from urllib import parse

from django import forms
from django.core import exceptions
from django.utils.translation import gettext as _

from replays import game_ids
from replays import models
from replays import limits

difficulty_names = (
    ("0", "Easy"),
    ("1", "Normal"),
    ("2", "Hard"),
    ("3", "Lunatic"),
    ("4", "Extra"),
    ("5", "Phantasm"),
)

category_names = [(category, name) for (category, name) in models.Category.choices]

replay_types = (
    ("1", _("Regular")),
    ("2", _("Stage Practice")),
    # ('3', _('Spell Practice)) # cannot support spell practice in games without replays that include the spellcard id
    ("4", _("PVP")),
)


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
    category = forms.ChoiceField(choices=category_names)
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


class PublishReplayWithoutFileForm(forms.Form):
    def __init__(self, *args, game: models.Game, **kwargs):
        super().__init__(*args, **kwargs)

        ShotField.set_queryset(self.fields["shot"], game.game_id)
        RouteField.set_queryset(self.fields["route"], game.game_id)

        if not self.fields["route"].should_include():
            del self.fields["route"]

        self.fields["difficulty"].choices = _GetDifficultyChoices(game)

        if not game_ids.HasBombs(game.game_id):
            del self.fields["uses_bombs"]
        if not game_ids.HasLives(game.game_id):
            del self.fields["misses"]

    difficulty = forms.ChoiceField(choices=difficulty_names, initial=1)
    shot = ShotField()
    route = RouteField()
    score = forms.IntegerField(min_value=0)
    category = forms.ChoiceField(choices=category_names)
    replay_type = forms.ChoiceField(choices=replay_types)
    is_clear = forms.BooleanField(initial=True, required=False)
    comment = _create_comment_field()
    video_link = VideoReplayLinkField(required=True)

    uses_bombs = forms.BooleanField(initial=True, required=False)
    misses = forms.IntegerField(required=False)


class EditReplayForm(forms.Form):
    comment = _create_comment_field()
