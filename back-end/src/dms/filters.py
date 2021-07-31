from django_filters import rest_framework as filters

from common.models.subjects import Subject

from dms.models.common import Author
from dms.models.papers import Paper
from dms.models.class_materials import (
    Section,
    Topic,
)
from dms.models.books import (
    Book,
    FavoriteBook,
)


class PaperFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="publication_date",
                                    lookup_expr="gte")
    end_date = filters.DateFilter(field_name="publication_date",
                                  lookup_expr="lte")
    category = filters.CharFilter(method="filter_by_category")

    def filter_by_category(self, queryset, name, value):
        # pylint: disable=unused-argument

        if value == "bin":
            return queryset.filter(is_binned=True)

        # TODO(TmLev): `int(value)` may throw on text inputs, although `value`
        #   should be an integer that represents category id.
        return queryset.filter(is_binned=False).filter(category=int(value))

    class Meta:
        model = Paper
        fields = ["authors", "category", "publishers", "user"]


class SectionFilter(filters.FilterSet):

    class Meta:
        model = Section
        fields = ["subject"]


class TopicFilter(filters.FilterSet):

    class Meta:
        model = Topic
        fields = ["section"]


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
    authors = filters.ModelMultipleChoiceFilter(
        field_name="book__authors",
        queryset=Author.objects.all(),
    )
    subjects = filters.ModelMultipleChoiceFilter(
        field_name="book__subjects",
        queryset=Subject.objects.all(),
    )

    class Meta:
        model = FavoriteBook
        exclude = ["user"]
