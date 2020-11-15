from django_filters import rest_framework as filters

from dms.models.papers import Paper


class PaperFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="publication_date",
                                    lookup_expr="gte")
    end_date = filters.DateFilter(field_name="publication_date",
                                  lookup_expr="lte")

    class Meta:
        model = Paper
        fields = ["authors", "category", "publishers"]
