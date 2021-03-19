from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from auth.models import Profile, ProfileUser


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.register(ProfileUser)
