from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_file, name='upload_file'),
    path('publish/<int:temp_replay_id>', views.publish_replay),
    path('publish/<str:game_id>', views.publish_replay_no_file),
    path('user/<str:username>', views.user_page),
    path('<str:game_id>', views.game_scoreboard),
    path('<str:game_id>/d<int:difficulty>', views.game_scoreboard),
    path('<str:game_id>/d<int:difficulty>/<str:shot_id>', views.game_scoreboard),
    path('<str:game_id>/<int:replay_id>', views.replay_details),
    path('<str:game_id>/<int:replay_id>/download', views.download_replay),
    path('<str:game_id>/<int:replay_id>/delete', views.delete_replay),
]
