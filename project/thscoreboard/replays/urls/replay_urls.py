from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import path

from replays.views import create_replay
from replays.views import index
from replays.views import reanalyze_all_replays
from replays.views import replay_list
from replays.views import user
from replays.views import view_replay


urlpatterns = [
    path("", index.index, name="index"),
    path("index/json", index.index_json),
    path("upload", create_replay.upload_file, name="upload_file"),
    path("publish/<int:temp_replay_id>", create_replay.publish_replay),
    path("publish/<str:game_id>", create_replay.publish_replay_no_file),
    path("user/", login_required(lambda req: redirect(f"/replays/user/{req.user}"))),
    path("user/<str:username>", user.user_page),
    path("user/<str:username>/json", user.user_page_json),
    path("reanalyze_all", reanalyze_all_replays.reanalyze_all),
    path("<str:game_id>", replay_list.game_scoreboard),
    path("<str:game_id>/json", replay_list.game_scoreboard_json),
    path("<str:game_id>/d<int:difficulty>", replay_list.game_scoreboard),
    path("<str:game_id>/d<int:difficulty>/<str:shot_id>", replay_list.game_scoreboard),
    path(
        "<str:game_id>/<int:replay_id>",
        view_replay.replay_details,
        name="Replays/Details",
    ),
    path("<str:game_id>/<int:replay_id>/edit", view_replay.edit_replay),
    path("<str:game_id>/<int:replay_id>/download", view_replay.download_replay),
    path("<str:game_id>/<int:replay_id>/delete", view_replay.delete_replay),
    path(
        "<str:game_id>/<int:replay_id>/reanalyze",
        view_replay.view_replay_reanalysis,
        name="Replays/Reanalysis",
    ),
]
