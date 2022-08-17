import logging
from django.shortcuts import render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators
from django.core.exceptions import ValidationError

from . import replay_parsing
from . import forms

@http_decorators.require_safe
def index(request):
    return render(request, 'scores/index.html')


class FileTooBigError(ValidationError):
    pass


def _ReadFile(file_from_form):
    """Read a file.
    
    Args:
        file_from_form: An UploadedFile.
    """
    if file_from_form.size > 1000000:
        raise FileTooBigError('Replays cannot be bigger than 1MB.')
    return file_from_form.read()


def _HandleReplay(request, replay_bytes):
    """Handle an uploaded replay.
    
    May raise ValidationError.
    """
    try:
        replay_parsing.Parse(replay_bytes)
    except replay_parsing.Error as e:
        raise ValidationError(str(e))


@auth_decorators.login_required
@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def upload_file(request):
    if request.method == 'POST':
        form = forms.UploadReplayFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file_contents = _ReadFile(request.FILES['replay_file'])
                logging.info('Replay was %s %d', type(file_contents), len(file_contents))
                replay_info = _HandleReplay(request, file_contents)
                # TODO: Save replay and redirect to sensible place
                return

            except ValidationError as e:
                form.add_error('replay_file', e)
    
    else:
        form = forms.UploadReplayFileForm()
        
    return render(request, 'scores/upload.html', {'form': form})
