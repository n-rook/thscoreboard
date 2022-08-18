import logging
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators
from django.core.exceptions import ValidationError

from . import forms
from . import limits
from . import models
from . import replay_parsing

@http_decorators.require_safe
def index(request):
    return render(request, 'scores/index.html')


# class FileTooBigError(ValidationError):
#     pass


def _ReadFile(file_from_form):
    """Read a file.
    
    Args:
        file_from_form: An UploadedFile.
    """
    if file_from_form.size > limits.MAX_REPLAY_SIZE:
        raise limits.FileTooBigError()
    return file_from_form.read()


def _HandleReplay(request, replay_bytes):
    """Handle an uploaded replay.
    
    May raise ValidationError.
    """
    try:
        return replay_parsing.Parse(replay_bytes)
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
                _ = _HandleReplay(request, file_contents)
                # We check that the replay can be parsed, but don't care about its
                # contents.

                temp_replay = models.TemporaryReplayFile(
                    user=request.user,
                    replay=file_contents
                )
                temp_replay.save()

                return redirect(
                    publish_replay,
                    temp_replay.id
                )



                return render(
                    request,
                    'scores/publish.html',
                    # Add params and stuff
                    # This should not be render... should be 304
                )


            except ValidationError as e:
                form.add_error('replay_file', e)
    
    else:
        form = forms.UploadReplayFileForm()

    return render(request, 'scores/upload.html', {'form': form})

@auth_decorators.login_required
@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def publish_replay(request, temp_replay_id):
    """The publish view is used to finalize uploaded replay files."""

    try:
        temp_replay = models.TemporaryReplayFile.objects.get(
            user=request.user,
            id=temp_replay_id)
    except models.TemporaryReplayFile.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        raise NotImplementedError()

    replay_info = replay_parsing.Parse(bytes(temp_replay.replay))
    form = forms.PublishReplayForm(initial={
        'difficulty': replay_info.difficulty,
        'shot': replay_info.shot,
        'score': replay_info.score
    })
    logging.info(replay_info.shot)
    # form.difficulty.initial = replay_info.difficulty
    # form.shot.initial = replay_info.shot
    # form.score.initial = replay_info.score
    
    return render(request, 'scores/publish.html', {'form': form})
