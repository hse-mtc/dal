from django_filters import rest_framework as filters

from dms.models.papers import Paper
from dms.models.books import Book
from dms.models.class_materials import Section


class PaperFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="publication_date",
                                    lookup_expr="gte")
    end_date = filters.DateFilter(field_name="publication_date",
                                  lookup_expr="lte")

    class Meta:
        model = Paper
        fields = ["authors", "category", "publishers"]


class SectionFilter(filters.FilterSet):

    class Meta:
        model = Section
        fields = ["subject"]


class BookFilter(filters.FilterSet):

    class Meta:
        model = Book
        fields = ["authors"]