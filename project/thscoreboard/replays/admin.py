"""Register administration hooks in this module."""

from django.contrib import admin

from replays import models

admin.site.register(models.Game)
admin.site.register(models.Shot)
admin.site.register(models.Route)
admin.site.register(models.Replay)
admin.site.register(models.ReplayStage)
admin.site.register(models.ReplayFile)
