import re

from common.models.subjects import Subject
from django.db.models import F, IntegerField, Q
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast
from django_filters import rest_framework as filters

from dms.models.books import (
    Book,
    FavoriteBook,
)
from dms.models.class_materials import (
    Section,
    Topic,
)
from dms.models.common import Author
from dms.models.papers import Paper


class PaperFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="publication_date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="publication_date", lookup_expr="lte")
    category = filters.CharFilter(method="filter_by_category")
    extra_filter = filters.BaseInFilter(field_name=None, method="filter_json")

    # Supported operators for filter tokens
    FILTER_OPERATORS = ("eq", "in", "contains", "lte", "gte")

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

    def _sanitize_alias(self, name):
        """
        Sanitize the alias name to be valid for Django annotations.
        Removes/replaces whitespace and other forbidden characters.
        """
        # Replace spaces with underscores, remove other problematic chars
        return re.sub(r'[\s"\';]', "_", name)

    def _split_filter_tokens(self, value):
        """
        Split a comma-separated filter string into individual tokens.

        Handles the case where user sends:
        "eq|field1|10,contains|field2|text"

        This should return: ["eq|field1|10", "contains|field2|text"]

        The tricky part is that `in` operator uses commas for values:
        "in|status|active,archived" should NOT be split.

        Solution: Split on comma followed by an operator prefix.
        """
        if not value:
            return []

        # Pattern: comma followed by one of the operators and a pipe
        # This splits: "eq|a|1,contains|b|2" -> ["eq|a|1", "contains|b|2"]
        # But preserves: "in|status|val1,val2" as one token
        ops_pattern = "|".join(self.FILTER_OPERATORS)
        split_pattern = rf",(?=(?:{ops_pattern})\|)"

        tokens = re.split(split_pattern, value)
        return [t.strip() for t in tokens if t.strip()]

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
                # Sanitize the annotation alias to avoid spaces and special chars
                ann_name = f"__{self._sanitize_alias(key)}_num_cast"
                expr = Cast(KeyTextTransform(key, F(json_field)), IntegerField())
                query = Q(**{f"{ann_name}__{op}": num}), {ann_name: expr}
            else:
                query = Q(**{f"{field_prefix}__{op}": val})

        return query

    def filter_json(self, queryset, name, value):
        # pylint: disable=unused-argument

        json_field = "additional_fields"
        queries = []
        all_annotations = {}

        for v in self.request.GET.getlist(name):
            # Split the value into individual tokens (handles comma-separated filters)
            tokens = self._split_filter_tokens(v)
            for token in tokens:
                build = self._build_q_from_token(token, json_field)
                if isinstance(build, tuple):
                    q, annotations = build
                    if annotations:
                        all_annotations.update(annotations)
                    queries.append(q)
                else:
                    queries.append(build)

        # Apply all annotations at once
        if all_annotations:
            queryset = queryset.annotate(**all_annotations)

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
