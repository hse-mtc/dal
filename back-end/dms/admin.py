from django.contrib import admin

from dms.models import (
    Author,
    Category,
    Paper,
    Publisher,
    Subject,
    File,
)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Paper)
admin.site.register(Publisher)
admin.site.register(Subject)
admin.site.register(File)
