"""Views related to creating a replay file."""

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators import http as http_decorators
from django.contrib.auth import decorators as auth_decorators
from django.core.exceptions import ValidationError

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
        temp_replay = models.TemporaryReplayFile.objects.get(
            user=request.user,
            id=temp_replay_id)
    except models.TemporaryReplayFile.DoesNotExist:
        raise Http404()

    replay_info = replay_parsing.Parse(bytes(temp_replay.replay))
    
    #   modify replays for fields that need to be adjusted to fit the db
    #   like foreign key fields and stuff

    shot_instance = models.Shot.objects.select_related('game').get(game=replay_info.game, shot_id=replay_info.shot)

    if replay_info.game in [game_ids.GameIDs.TH01, game_ids.GameIDs.TH08]:
        replay_info.route = models.Route.objects.select_related('game').get(game=replay_info.game, route_id=replay_info.route)

    if request.method == 'POST':
        form = forms.PublishReplayForm(replay_info.game, request.POST)
        if form.is_valid():
            new_replay = create_replay.PublishNewReplay(
                user=request.user,
                difficulty=replay_info.difficulty,
                shot=shot_instance,
                score=form.cleaned_data['score'],
                category=form.cleaned_data['category'],
                comment=form.cleaned_data['comment'],
                is_good=form.cleaned_data['is_good'],
                is_clear=form.cleaned_data['is_clear'],
                video_link=form.cleaned_data['video_link'],
                temp_replay_instance=temp_replay,
                replay_info=replay_info
            )
            return redirect(view_replay.replay_details, game_id=replay_info.game, replay_id=new_replay.id)
        else:
            return render(request, 'replays/publish.html', {'form': form})

    form = forms.PublishReplayForm(
        replay_info.game,
        initial={
            'score': replay_info.score,
            'name': replay_info.name
        })

    context = {
        'form': form,
        'game_name': shot_instance.game.GetName(),
        'game_id': shot_instance.game.game_id,
        'difficulty_name': shot_instance.game.GetDifficultyName(replay_info.difficulty),
        'shot_name': shot_instance.GetName(),
        'route_name': None,
        'has_replay_file': True,
        'replay': replay_info,
    }

    if replay_info.route:
        context['route_name'] = replay_info.route.GetName()

    # When IN is supported, add "route" here too.

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
