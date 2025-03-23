from common.models.recruitment_office import RecruitmentOffice

from drf_spectacular.views import extend_schema

from rest_framework import generics

from common.serializers.recruitment_office import RecruitmentOfficeSerializer


@extend_schema(tags=["recruitment-offices"])
class RecruitmentOfficeView(generics.ListAPIView):
    queryset = RecruitmentOffice.objects.all()
    serializer_class = RecruitmentOfficeSerializer
