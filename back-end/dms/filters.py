from django_filters import rest_framework as filters

from dms.models.papers import Paper
from dms.models.class_materials import Section
from common.models.subjects import Subject
from dms.models.books import (
    Book,
    FavoriteBook,
)


class PaperFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="publication_date",
                                    lookup_expr="gte")
    end_date = filters.DateFilter(field_name="publication_date",
                                  lookup_expr="lte")

    class Meta:
        model = Paper
        fields = ["authors", "category", "publishers", "user"]


class SectionFilter(filters.FilterSet):

    class Meta:
        model = Section
        fields = ["subject"]


class BookFilter(filters.FilterSet):
    start_year = filters.NumberFilter(field_name="publication_year",
                                      lookup_expr="gte")
    end_year = filters.NumberFilter(field_name="publication_year",
                                    lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["authors", "user", "subjects"]


class SubjectFilter(filters.FilterSet):

    class Meta:
        model = Subject
        fields = ["user"]


class FavoriteBookFilter(filters.FilterSet):
    start_year = filters.NumberFilter(field_name="book__publication_year",
                                          lookup_expr="gte")
    end_year = filters.NumberFilter(field_name="book__publication_year",
                                        lookup_expr="lte")

    class Meta:
        model = FavoriteBook
        fields = ["user", "book__authors", "book__subjects"]
