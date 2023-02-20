"""Views related to creating a replay file."""

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators
from django.core.exceptions import ValidationError

from replays import constant_helpers
from replays import create_replay
from replays import forms
from replays import limits
from replays import models
from replays import replay_parsing
from replays import game_ids
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
                replay_info = _HandleReplay(request, file_contents)
                replay = create_replay.PublishNewReplay(
                    request.user,
                    models.Category.PENDING,
                    '', '', None, None,
                    file_contents, replay_info
                )
                # We check that the replay can be parsed, but don't care about its
                # contents.

                return redirect(
                    publish_replay,
                    replay.id
                )

            except ValidationError as e:
                form.add_error('replay_file', e)

    else:
        form = forms.UploadReplayFileForm()

    all_games = models.Game.objects.all()
    replay_games = [g for g in all_games if g.has_replays]
    no_replay_games = [g for g in all_games if not g.has_replays]

    return render(
        request,
        'replays/upload.html',
        {
            'form': form,
            'all_games': all_games,
            'replay_games': replay_games,
            'no_replay_games': no_replay_games,
        }
    )


@auth_decorators.login_required
@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def publish_replay(request, temp_replay_id):
    """The publish view is used to finalize uploaded replay files."""

    try:
        replay = models.Replay.objects.get(
            user=request.user,
            id=temp_replay_id)
        shot = models.Shot.objects.get(id=replay.shot_id)
    except (models.Replay.DoesNotExist, models.Shot.DoesNotExist):
        raise Http404()

    if request.method == 'POST':
        form = forms.PublishReplayForm(shot.game, request.POST)
        if form.is_valid():

            if shot.game == game_ids.GameIDs.TH09:
                replay.score = form.cleaned_data['score']

            replay.category = form.cleaned_data['category']
            replay.comment = form.cleaned_data['comment']
            replay.is_good = form.cleaned_data['is_good']
            replay.is_clear = form.cleaned_data['is_clear']
            replay.video_link = form.cleaned_data['video_link']

            replay.save()

            return redirect(view_replay.replay_details, game_id=shot.game, replay_id=replay.id)
        else:
            return render(request, 'replays/publish.html', {'form': form})

    constants = constant_helpers.GetModelInstancesForReplay(shot.game, shot.shot_id, replay.route)

    form = forms.PublishReplayForm(
        shot.game,
        initial={
            'score': replay.score,
            'category': replay.category if replay.category != models.Category.PENDING else None,
            'comment': replay.comment,
            'is_good': replay.is_good if replay.is_good is not None else True,
            'is_clear': replay.is_clear if replay.is_clear is not None else True,
            'video_link': replay.video_link,
            'name': replay.name
        })

    context = {
        'form': form,
        'game_name': constants.game.GetName(),
        'game_id': constants.game.game_id,
        'difficulty_name': constants.game.GetDifficultyName(replay.difficulty),
        'shot_name': constants.shot.GetName(),
        'route_name': None,
        'has_replay_file': True,
        'replay': replay,
        'replay_type': game_ids.GetReplayType(replay.replay_type)
    }

    if replay.route:
        context['route_name'] = constants.route.GetName()

    return render(request, 'replays/publish.html', context)


@auth_decorators.login_required
@http_decorators.require_http_methods(['GET', 'HEAD', 'POST'])
def publish_replay_no_file(request, game_id: str):
    """Publish a replay for a game without replays."""
    game = get_object_or_404(models.Game, game_id=game_id, has_replays=False)

    if request.method == 'POST':
        form = forms.PublishReplayWithoutFileForm(request.POST, game=game)
        if form.is_valid():
            new_replay = create_replay.PublishReplayWithoutFile(
                user=request.user,
                difficulty=form.cleaned_data['difficulty'],
                shot=form.cleaned_data['shot'],
                route=form.cleaned_data.get('route'),  # Passes None if route is not defined.
                score=form.cleaned_data['score'],
                category=form.cleaned_data['category'],
                is_clear=form.cleaned_data['is_clear'],
                comment=form.cleaned_data['comment'],
                video_link=form.cleaned_data['video_link'],
                replay_type=form.cleaned_data['replay_type']
            )
            return redirect(view_replay.replay_details, game_id=game.game_id, replay_id=new_replay.id)
        else:
            return render(
                request,
                'replays/publish_no_replay.html',
                {
                    'game': game,
                    'form': form,
                    'has_replay_file': False
                }
            )

    form = forms.PublishReplayWithoutFileForm(game=game)
    return render(
        request,
        'replays/publish_no_replay.html',
        {
            'game': game,
            'form': form,
            'has_replay_file': False
        }
    )
