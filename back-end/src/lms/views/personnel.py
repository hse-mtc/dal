from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.views import (
    extend_schema,
    OpenApiParameter,
)

from lms.models.students import Student
from lms.models.teachers import Teacher

from lms.serializers.personnel import (
    SearchPersonnelUsersSerializer,
    PersonnelUsersSerializer,
)


@extend_schema(
    tags=["personnel"],
    parameters=[
        OpenApiParameter(
            name="name",
            description="Filter by full name",
            required=True,
        ),
    ],
)
class SearchPersonnelUsersViewSet(ListModelMixin, GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = PersonnelUsersSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        serializer = SearchPersonnelUsersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data["name"]
        query = (Q(surname__icontains=name) | Q(name__icontains=name) |
                 Q(patronymic__icontains=name))

        results = []

        for model in [Student, Teacher]:
            queryset = model.objects.filter(user__isnull=False).filter(query)
            serializer = PersonnelUsersSerializer(queryset, many=True)
            results.extend(serializer.data)

        return Response(data=results)
