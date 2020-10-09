from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from lms.serializers.reference_book import ReferenceBookSerializer


class ReferenceBookView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        resp = ReferenceBookSerializer(data={})
        resp.is_valid()
        return Response(resp.data)
