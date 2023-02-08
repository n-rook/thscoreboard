from django.contrib import admin

from . import models

admin.site.register(models.EarlyAccessPasscode)
admin.site.register(models.User)
admin.site.register(models.UnverifiedUser)
admin.site.register(models.InvitedUser)
admin.site.register(models.UserPasscodeTie)
admin.site.register(models.IPBan)
admin.site.register(models.Ban)
