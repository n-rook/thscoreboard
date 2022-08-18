from distutils.command.upload import upload
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_file, name='upload_file'),
    path('publish/<int:temp_replay_id>', views.publish_replay),
]
