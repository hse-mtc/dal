from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from backend.models import (
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


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Document)
admin.site.register(Publisher)
admin.site.register(Subject)
