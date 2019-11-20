from django.contrib import admin
from herokuapp.models import UserProfileInfo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserProfileInfoInline(admin.StackedInline):
    model = UserProfileInfo
    verbose_name_plural = 'User data'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInfoInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.
