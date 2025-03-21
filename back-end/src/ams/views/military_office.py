from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from common.models.military import MilitaryOffice
from ams.serializers.military_office import MilitaryOfficeSerializer


class MilitaryOfficeViewSet(ModelViewSet):
    queryset = MilitaryOffice.objects.all()
    serializer_class = MilitaryOfficeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'city', 'code']
