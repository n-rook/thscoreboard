import logging
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators
from django.core.exceptions import ValidationError
from django.db import transaction

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

    replay_info = replay_parsing.Parse(bytes(temp_replay.replay))

    if request.method == 'POST':
        form = forms.PublishReplayForm(request.POST)
        if form.is_valid():
            PublishNewScore(
                user=request.user,
                game_id=replay_info.game,
                difficulty=replay_info.difficulty,
                shot_id=replay_info.shot,
                points=form.cleaned_data['points'],
                category=form.cleaned_data['category'],
                comment=form.cleaned_data['comment'],
                is_good=form.cleaned_data['is_good'],
                temp_replay_instance=temp_replay,
                replay_info=replay_info,
            )
            # 304 over to replay details page
            raise NotImplementedError()
        else:
            return render(request, 'scores/publish.html', {'form': form})

    form = forms.PublishReplayForm(initial={
        'difficulty': replay_info.difficulty,
        'shot': replay_info.shot,
        'points': replay_info.score
    })
    # form.difficulty.initial = replay_info.difficulty
    # form.shot.initial = replay_info.shot
    # form.score.initial = replay_info.score
    
    return render(request, 'scores/publish.html', {'form': form})

@transaction.atomic
def PublishNewScore(user, game_id: str, difficulty: int, shot_id: str, points: int, category: str, comment: str, is_good: bool, temp_replay_instance: models.TemporaryReplayFile, replay_info: replay_parsing.ReplayInfo):
    shot_instance = models.Shot.objects.select_related('game').get(game=game_id, shot_id=shot_id)

    score_instance = models.Score(
        user=user,
        shot=shot_instance,
        difficulty=difficulty,
        points=points,
        category=category,
        comment=comment,
    )
    replay_file_instance = models.ReplayFile(
        score=score_instance,
        replay=temp_replay_instance.replay,
        is_good=is_good,
        points=replay_info.score,
    )
    
    score_instance.save()
    replay_file_instance.save()
    temp_replay_instance.delete()
