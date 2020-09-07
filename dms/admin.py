from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from dms.models import (
    Author,
    Category,
    Document,
    Profile,
    Publisher,
    Subject,
)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInline,
    ]


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Document)
admin.site.register(Publisher)
admin.site.register(Subject)
