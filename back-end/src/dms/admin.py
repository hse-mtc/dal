from django.contrib import admin

from dms.models.books import (
    Cover,
    Book,
    FavoriteBook,
)
from dms.models.documents import File
from dms.models.papers import (
    Category,
    Paper,
)
from dms.models.class_materials import (
    ClassMaterial,
    Section,
    Topic,
)
from dms.models.common import (
    Author,
    Publisher,
)

admin.site.register(Author)
admin.site.register(Cover)
admin.site.register(Book)
admin.site.register(FavoriteBook)
admin.site.register(Category)
admin.site.register(ClassMaterial)
admin.site.register(Publisher)
admin.site.register(Section)
admin.site.register(Topic)
admin.site.register(File)


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_filter = ["category"]
