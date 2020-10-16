from django.contrib import admin

from dms.models import (
    Author,
    Category,
    ClassMaterial,
    File,
    Paper,
    Publisher,
    Subject,
)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(ClassMaterial)
admin.site.register(File)
admin.site.register(Paper)
admin.site.register(Publisher)
admin.site.register(Subject)
