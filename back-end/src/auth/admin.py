from django.contrib import admin
from django.contrib.auth import get_user_model

from auth.models import Permission, Group

admin.site.register(get_user_model())

admin.site.register(Permission)
admin.site.register(Group)
