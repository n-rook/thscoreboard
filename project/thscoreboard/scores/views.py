import logging
from urllib import parse

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
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
            new_score = PublishNewScore(
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
            return redirect(score_details, game_id=replay_info.game, score_id=new_score.id)
        else:
            return render(request, 'scores/publish.html', {'form': form})

    form = forms.PublishReplayForm(initial={
        'difficulty': replay_info.difficulty,
        'shot': replay_info.shot,
        'points': replay_info.score
    })
    
    return render(request, 'scores/publish.html', {'form': form})


@http_decorators.require_safe
def score_details(request, game_id: str, score_id: int):
    score_instance = GetScoreOr404(request.user, game_id)

    if score_instance.shot.game.game_id != game_id:
        # Wrong game, but IDs are unique anyway so we know the right game. Send the user there.
        return redirect(score_details, game_id=score_instance.shot.game.game_id, score_id=score_id)

    return render(request, 'scores/score_details.html', {
        'game_name': score_instance.shot.game.GetName(),
        'shot_name': score_instance.shot.GetName(),
        'difficulty_name': score_instance.GetDifficultyName(),
        'game_id': game_id,
        'score': score_instance,
        'replay': score_instance.replayfile,
        'is_owner': request.user == score_instance.user,
    })


@http_decorators.require_safe
def download_replay(request, game_id: str, score_id: int):
    score_instance = GetScoreOr404(request.user, score_id)
    
    if score_instance.shot.game.game_id != game_id:
        raise Http404()
    if not score_instance.shot.game.has_replays:
        raise HttpResponseBadRequest()
    
    try:
        replay_instance = models.ReplayFile.objects.get(score=score_instance)
    except models.ReplayFile.DoesNotExist:
        raise ValueError('No replay for this score. This should not be possible')
    
    content_disposition = 'attachment; filename="{basic_filename}"; filename*=UTF-8''{utf8_filename}'.format(
        basic_filename=score_instance.GetNiceFilename(ascii_only=True),
        utf8_filename=parse.quote_plus(score_instance.GetNiceFilename(), encoding='UTF-8')
    )

    return HttpResponse(
        replay_instance.replay,
        headers={
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': content_disposition
        }
    )

@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
@auth_decorators.login_required
def delete_score(request, game_id: str, score_id: int):
    score_instance = GetScoreOr404(request.user, score_id)

    if score_instance.shot.game.game_id != game_id:
        raise Http404()
    if not score_instance.user == request.user:
        raise HttpResponseForbidden()
    
    if request.method == 'POST':
        score_instance.delete()
        return redirect(f'/scores/user/{request.user.username}')
    
    return render(
        request,
        'scores/delete_score.html',
        {   
            'game_name': score_instance.shot.game.GetName(),
            'shot_name': score_instance.shot.GetName(),
            'difficulty_name': score_instance.GetDifficultyName(),
            'score': score_instance,
        }
    )


def GetScoreOr404(user, score_id):
    try:
        score_instance = models.Score.objects.select_related('shot').get(id=score_id)
    except models.Score.DoesNotExist:
        raise Http404()
    if not score_instance.IsVisible(user):
        raise Http404()
    return score_instance


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
    return score_instance
