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
from django.db.models import Q, F, IntegerField
from django.db.models.functions import Cast
from django.db.models.fields.json import KeyTextTransform

from django.db.models import Q


class PaperFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="publication_date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="publication_date", lookup_expr="lte")
    category = filters.CharFilter(method="filter_by_category")
    extra_filter = filters.BaseInFilter(field_name=None, method="filter_json")

    def filter_by_category(self, queryset, name, value):
        # pylint: disable=unused-argument

        if value == "bin":
            return queryset.filter(is_binned=True)
        return queryset.filter(is_binned=False, category=int(value))

    def _parse_number(self, s):
        try:
            return int(s)
        except:
            return None

    def _build_q_from_token(self, token, json_field):
        """
        token format: <op>|<key>|<value> where op in (eq, in, contains, lte, gte)
        """
        parts = token.split("|", 2)
        if len(parts) < 3:
            return Q()
        op, key, val = parts[0], parts[1], parts[2]
        field_prefix = f"{json_field}__{key}"
        query = Q()

        if op == "eq":
            num = self._parse_number(val)
            if num is None:
                query = Q(**{field_prefix: val})
            else:
                query = Q(**{field_prefix: num})
                query |= Q(**{field_prefix: val})
        elif op == "in":
            items = [i for i in val.split(",") if i != ""]
            query = Q(**{f"{field_prefix}__in": items})
        elif op == "contains":
            query = Q(**{f"{field_prefix}__icontains": val})
        if op in ("lte", "gte"):
            num = self._parse_number(val)
            if num is not None:
                ann_name = f"__{key}_num_cast"
                expr = Cast(KeyTextTransform(key, F(json_field)), IntegerField())
                query = Q(**{f"{ann_name}__{op}": num}), {ann_name: expr}
            else:
                query = Q(**{f"{field_prefix}__{op}": val})

        return query

    def filter_json(self, queryset, name, value):
        # pylint: disable=unused-argument

        json_field = "additional_fields"
        queries = []
        for v in self.request.GET.getlist(name):
            build = self._build_q_from_token(v, json_field)
            if isinstance(build, tuple):
                q, annotations = build
                if annotations:
                    queryset = queryset.annotate(**annotations)
                queries.append(q)
            else:
                queries.append(build)

        q = Q()
        for query in queries:
            q = q & query

        return queryset.filter(q)

    class Meta:
        model = Paper
        fields = ["authors", "category", "publishers", "user", "extra_filter"]


class SectionFilter(filters.FilterSet):
    class Meta:
        model = Section
        fields = ["subject"]


class TopicFilter(filters.FilterSet):
    class Meta:
        model = Topic
        fields = ["section"]


class BookFilter(filters.FilterSet):
    start_year = filters.NumberFilter(field_name="publication_year", lookup_expr="gte")
    end_year = filters.NumberFilter(field_name="publication_year", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["authors", "user", "subjects"]


class SubjectFilter(filters.FilterSet):
    class Meta:
        model = Subject
        fields = ["user", "milspecialty"]


class FavoriteBookFilter(filters.FilterSet):
    start_year = filters.NumberFilter(
        field_name="book__publication_year", lookup_expr="gte"
    )
    end_year = filters.NumberFilter(
        field_name="book__publication_year", lookup_expr="lte"
    )
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
