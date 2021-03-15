from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from auth.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
