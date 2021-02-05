from django.contrib import admin

from dms.models.books import (
    Book,
    FavoriteBook,
)
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
admin.site.register(Book)
admin.site.register(FavoriteBook)
admin.site.register(Category)
admin.site.register(ClassMaterial)
admin.site.register(Paper)
admin.site.register(Publisher)
admin.site.register(Section)
admin.site.register(Topic)
