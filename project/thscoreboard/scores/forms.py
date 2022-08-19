from urllib import parse

from django import forms
from django.core import validators
from django.core import exceptions

from . import models
from . import limits

game_names = (
    ('th06', '東方紅魔郷 - Embodiment of Scarlet Devil'),
)

difficulty_names = (
    ('0', 'Easy'),
    ('1', 'Normal'),
    ('2', 'Hard'),
    ('3', 'Lunatic'),
    ('4', 'Extra'),
)

shot_names = (
    ('ReimuA', 'Reimu A'),
    ('ReimuB', 'Reimu B'),
    ('MarisaA', 'Marisa A'),
    ('MarisaB', 'Marisa B'),
)

category_names = (
    ('regular', 'Regular'),
    ('tas', 'Tool-Assisted'),
    ('unranked', 'Unranked'),
    ('private', 'Private')
)


_ALLOWED_REPLAY_HOSTS = [
    'www.youtube.com',
    'youtu.be',
]


def _AllowedVideoDomainsValidator(value: str):
    split_url = parse.urlsplit(value)
    if split_url.hostname not in _ALLOWED_REPLAY_HOSTS:
        raise exceptions.ValidationError(
            'If present, the replay link must be to one of the following sites: %(sites_comma_separated)s',
            params={
                'sites_comma_separated': ', '.join(_ALLOWED_REPLAY_HOSTS)
            }
            )


class ShotField(forms.ModelChoiceField):
    """A field defining shot type. You must call set_queryset before using."""

    def __init__(self):
        super().__init__(
            queryset=None,
            empty_label=None,
            )
    
    @classmethod
    def set_queryset(self, field: 'ShotField', game_id: str):
        field.queryset = models.Shot.objects.filter(game=game_id)

    def label_from_instance(self, obj: models.Shot) -> str:
        return obj.GetName()


class VideoReplayLinkField(forms.URLField):
    default_validators = forms.URLField.default_validators + [_AllowedVideoDomainsValidator]


# TODO: Fix up so that these settings are set dynamically based on game

class UploadReplayFileForm(forms.Form):
    replay_file = forms.FileField()
    
class PublishReplayForm(forms.Form):

    def __init__(self, *args, game_id: str, **kwargs):
        super().__init__(*args, **kwargs)

        ShotField.set_queryset(self.fields['shot'], game_id)

    difficulty = forms.ChoiceField(choices=difficulty_names)
    shot = ShotField()
    points = forms.IntegerField(min_value=0)
    category = forms.ChoiceField(choices=models.Category.choices)
    comment = forms.CharField(max_length=limits.MAX_COMMENT_LENGTH, required=False)
    is_good = forms.BooleanField(initial=True, required=False)
    video_link = VideoReplayLinkField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['is_good'] and not cleaned_data['video_link']:
            self.add_error('video_link', 
            exceptions.ValidationError(
                'If your replay desyncs, please provide a video so it can still be watched.'))


class PublishScoreWithoutReplayForm(forms.Form):

    def __init__(self, *args, game_id: str, **kwargs):
        super().__init__(*args, **kwargs)

        ShotField.set_queryset(self.fields['shot'], game_id)

    difficulty = forms.ChoiceField(choices=difficulty_names)
    shot = ShotField()
    points = forms.IntegerField(min_value=0)
    category = forms.ChoiceField(choices=models.Category.choices)
    comment = forms.CharField(max_length=limits.MAX_COMMENT_LENGTH, required=False)
    video_link = VideoReplayLinkField(required=True)
