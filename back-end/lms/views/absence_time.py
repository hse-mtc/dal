from rest_framework.permissions import AllowAny

from rest_framework.generics import RetrieveUpdateAPIView

from drf_spectacular.views import extend_schema

from lms.models.absence import AbsenceTime
from lms.serializers.absence import AbsenceTimeSerializer


@extend_schema(tags=['absence_time'])
class AbsenceTimeView(RetrieveUpdateAPIView):
    serializer_class = AbsenceTimeSerializer
    queryset = AbsenceTime.objects.all()

    permission_classes = [AllowAny]

    def get_object(self) -> AbsenceTime:
        obj = AbsenceTime.objects.last()

        self.check_object_permissions(self.request, obj)

        return obj
