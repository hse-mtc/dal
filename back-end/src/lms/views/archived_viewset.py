from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS


class ArchivedModelViewSet(ModelViewSet):

    def get_queryset(self):
        if (self.request.method in SAFE_METHODS and
                "archived" not in self.request.query_params):
            return self.queryset.filter(student__milgroup__archived=False)
        return super().get_queryset()
