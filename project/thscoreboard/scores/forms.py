from django import forms

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

# TODO: Fix up so that these settings are set dynamically based on game

class UploadReplayFileForm(forms.Form):
    replay_file = forms.FileField()
    
class PublishReplayForm(forms.Form):
    # game = forms.ChoiceField(choices=game_names)
    difficulty = forms.ChoiceField(choices=difficulty_names)
    shot = forms.ChoiceField(choices=shot_names)
    points = forms.IntegerField(min_value=0)
    category = forms.ChoiceField(choices=models.Category.choices)
    comment = forms.CharField(max_length=limits.MAX_COMMENT_LENGTH, required=False)
    is_good = forms.BooleanField(initial=True)
