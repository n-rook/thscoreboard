"""Views related to creating a replay file."""

import logging

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators
from django.core.exceptions import ValidationError
from django.db import transaction

from replays import forms
from replays import limits
from replays import models
from replays import replay_parsing
from replays.views import view_replay


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
    
    all_games = models.Game.objects.all()
    no_replay_games = [g for g in all_games if not g.has_replays]

    return render(
        request,
        'replays/upload.html',
        {
            'form': form,
            'all_games': all_games,
            'no_replay_games': no_replay_games,
        }
    )


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
    shot_instance = models.Shot.objects.select_related('game').get(game=replay_info.game, shot_id=replay_info.shot)

    if request.method == 'POST':
        form = forms.PublishReplayForm(request.POST, game_id=replay_info.game)
        if form.is_valid():
            new_replay = PublishNewReplay(
                user=request.user,
                # game_id=replay_info.game,
                difficulty=replay_info.difficulty,
                # shot_id=replay_info.shot,
                shot=shot_instance,
                points=form.cleaned_data['points'],
                category=form.cleaned_data['category'],
                comment=form.cleaned_data['comment'],
                is_good=form.cleaned_data['is_good'],
                video_link=form.cleaned_data['video_link'],
                temp_replay_instance=temp_replay,
                replay_info=replay_info,
            )
            return redirect(view_replay.replay_details, game_id=replay_info.game, replay_id=new_replay.id)
        else:
            return render(request, 'replays/publish.html', {'form': form})

    form = forms.PublishReplayForm(
        game_id=replay_info.game,
        initial={
            'difficulty': replay_info.difficulty,
            'shot': shot_instance,
            'points': replay_info.score
        })
    
    return render(
        request,
        'replays/publish.html',
        {
            'form': form,
            'has_replay_file': True,
        }
    )


@auth_decorators.login_required
@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def publish_replay_no_file(request, game_id: str):
    """Publish a replay for a game without replays."""
    game = get_object_or_404(models.Game, game_id=game_id, has_replays=False)

    if request.method == 'POST':
        form = forms.PublishReplayWithoutFileForm(request.POST, game_id=game.game_id)
        if form.is_valid():
            new_replay = PublishReplayWithoutFile(
                user=request.user,
                difficulty=form.cleaned_data['difficulty'],
                shot=form.cleaned_data['shot'],
                points=form.cleaned_data['points'],
                category=form.cleaned_data['category'],
                comment=form.cleaned_data['comment'],
                video_link=form.cleaned_data['video_link'],
            )
            return redirect(view_replay.replay_details, game_id=game.game_id, replay_id=new_replay.id)
        else:
            return render(
                request,
                'replays/publish.html',
                {
                    'game': game,
                    'form': form,
                    'has_replay_file': False
                }
            )
    
    form = forms.PublishReplayWithoutFileForm(game_id=game.game_id)
    return render(
        request,
        'replays/publish_no_replay.html',
        {
            'game': game,
            'form': form,
            'has_replay_file': False
        }
    )


@transaction.atomic
def PublishNewReplay(user, difficulty: int, shot: models.Shot, points: int, category: str, comment: str, video_link: str, is_good: bool, temp_replay_instance: models.TemporaryReplayFile, replay_info: replay_parsing.ReplayInfo):
    # shot_instance = models.Shot.objects.select_related('game').get(game=game_id, shot_id=shot_id)

    replay_instance = models.Replay(
        user=user,
        shot=shot,
        difficulty=difficulty,
        points=points,
        category=category,
        comment=comment,
        video_link=video_link,
        is_good=is_good,
        rep_points=replay_info.score,
    )
    replay_file_instance = models.ReplayFile(
        replay=replay_instance,
        replay_file=temp_replay_instance.replay,
    )

    replay_instance.save()
    replay_file_instance.save()
    temp_replay_instance.delete()
    return replay_instance


def PublishReplayWithoutFile(user, difficulty: int, shot: models.Shot, points: int, category: str, comment: str, video_link: str):
    replay_instance = models.Replay(
        user=user,
        shot=shot,
        difficulty=difficulty,
        points=points,
        category=category,
        comment=comment,
        video_link=video_link
    )
    replay_instance.save()
    return replay_instance
