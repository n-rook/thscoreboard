import logging
from typing import Optional
from urllib import parse


from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators import http as http_decorators
from django.contrib import auth
from django.contrib.auth import decorators as auth_decorators
from django.core.exceptions import ValidationError
from django.db import transaction

from . import forms
from . import limits
from . import models
from . import replay_parsing
from . import game_ids


@http_decorators.require_safe
def index(request):
    all_games = models.Game.objects.all()

    recent_uploads = (
        models.Replay.objects
        .filter(category__in=[models.Category.REGULAR, models.Category.TAS])
        .order_by('-created')
        [:10]
    )

    return render(
        request, 'replays/index.html',
        {
            'all_games': all_games,
            'recent_uploads': recent_uploads,
        })


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
            return redirect(replay_details, game_id=replay_info.game, replay_id=new_replay.id)
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
            return redirect(replay_details, game_id=game.game_id, replay_id=new_replay.id)
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
    

@http_decorators.require_safe
def replay_details(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        # Wrong game, but IDs are unique anyway so we know the right game. Send the user there.
        return redirect(replay_details, game_id=replay_instance.shot.game.game_id, replay_id=replay_id)

    context = {
        'game_name': replay_instance.shot.game.GetName(),
        'shot_name': replay_instance.shot.GetName(),
        'difficulty_name': replay_instance.GetDifficultyName(),
        'game_id': game_id,
        'replay': replay_instance,
        'is_owner': request.user == replay_instance.user,
    }
    if hasattr(replay_instance, 'replayfile'):
        context['has_replay_file'] = True
        context['replay_file_is_good'] = replay_instance.replayfile.is_good
    else:
        context['has_replay_file'] = False

    return render(request, 'replays/replay_details.html', context)


@http_decorators.require_safe
def download_replay(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)
    
    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    if not replay_instance.shot.game.has_replays:
        raise HttpResponseBadRequest()
    
    try:
        replay_file_instance = models.ReplayFile.objects.get(replay=replay_instance)
    except models.ReplayFile.DoesNotExist:
        raise ValueError('No replay file for this submission. This should not be possible')
    
    content_disposition = 'attachment; filename="{basic_filename}"; filename*={utf8_filename}'.format(
        basic_filename=replay_instance.GetNiceFilename(ascii_only=True),
        utf8_filename=parse.quote_plus(replay_instance.GetNiceFilename(), encoding='UTF-8')
    )

    return HttpResponse(
        replay_file_instance.replay_file,
        headers={
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': content_disposition
        }
    )


@http_decorators.require_safe
def game_scoreboard(request, game_id: str, difficulty: Optional[int] = None, shot_id: Optional[str] = None):
    # Ancient wisdom: You don't need pagination if you don't have users yet!
    game = get_object_or_404(models.Game, game_id=game_id)
    all_replays = (
        models.Replay.objects.select_related('shot', 'replayfile')
        .filter(category=models.Category.REGULAR)
        .filter(shot__game=game_id)
        .order_by('-points')
    )
    extra_params = {}
    if difficulty is not None:
        if difficulty < 0 or difficulty >= game.num_difficulties:
            raise Http404()
        all_replays = all_replays.filter(difficulty=difficulty)
        extra_params['difficulty'] = difficulty
        extra_params['difficulty_name'] = game_ids.GetDifficultyName(game.game_id, difficulty)

    if shot_id is not None:
        shot = get_object_or_404(models.Shot, game=game_id, shot_id=shot_id)
        all_replays = all_replays.filter(shot=shot)
        extra_params['shot'] = shot

    return render(
        request,
        'replays/game_scoreboard.html',
        {
            'game': game,
            'replays': all_replays,
            **extra_params
        })


@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def user_page(request, username: str):
    user = get_object_or_404(auth.get_user_model(), username=username)
    
    def GetUserReplays():
        # Yields (game, list_of_replays_for_the_game) tuples.
        
        replays = (
            models.Replay.objects
            .filter(user=user)
            .exclude(category=models.Category.PRIVATE)
            .order_by('shot__game_id', 'shot_id', 'created'))
        
        current_game = None
        for replay in replays:
            if current_game is None:
                current_game = replay.shot.game
                current_replays = []
            if current_game != replay.shot.game:
                yield (current_game, current_replays)
                current_game = replay.shot.game
                current_replays = []
            current_replays.append(replay)
        if current_game is not None:
            yield (current_game, current_replays)

    return render(
        request,
        'replays/user_page.html',
        {
            'viewed_user': user,
            'replays_by_game': list(GetUserReplays())
        }
    )
    

@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
@auth_decorators.login_required
def delete_replay(request, game_id: str, replay_id: int):
    replay_instance = GetReplayOr404(request.user, replay_id)

    if replay_instance.shot.game.game_id != game_id:
        raise Http404()
    if not replay_instance.user == request.user:
        raise HttpResponseForbidden()
    
    if request.method == 'POST':
        replay_instance.delete()
        return redirect(f'/replays/user/{request.user.username}')
    
    return render(
        request,
        'replays/delete_replay.html',
        {
            'game_name': replay_instance.shot.game.GetName(),
            'shot_name': replay_instance.shot.GetName(),
            'difficulty_name': replay_instance.GetDifficultyName(),
            'replay': replay_instance,
        }
    )


def GetReplayOr404(user, replay_id):
    try:
        replay_instance = models.Replay.objects.select_related('shot').get(id=replay_id)
    except models.Replay.DoesNotExist:
        raise Http404()
    if not replay_instance.IsVisible(user):
        raise Http404()
    return replay_instance


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
    )
    replay_file_instance = models.ReplayFile(
        replay=replay_instance,
        replay_file=temp_replay_instance.replay,
        is_good=is_good,
        points=replay_info.score,
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
