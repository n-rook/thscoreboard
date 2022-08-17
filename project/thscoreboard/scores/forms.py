from django import forms

class UploadReplayFileForm(forms.Form):
    replay_file = forms.FileField()
    