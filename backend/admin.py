from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from backend import models


class ProfileInline(admin.StackedInline):
    model = models.Profile


class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models.Author)
admin.site.register(models.Document)
admin.site.register(models.Publisher)
admin.site.register(models.Subject)
admin.site.register(models.Section)
admin.site.register(models.Topic)
