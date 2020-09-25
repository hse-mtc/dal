from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend


# pylint: disable=not-callable
class GetPutPostDeleteModelViewSet(ModelViewSet):
    query_params_serializer_class = None

    filter_backends = [DjangoFilterBackend, SearchFilter]

    class Meta:
        abstract = True

    def list(self, request: Request) -> Response:
        # pylint: disable=no-member
        # check query params
        query_params = self.query_params_serializer_class(
            data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=HTTP_400_BAD_REQUEST)

        return super().list(request)

    def retrieve(self, request: Request, pk: int) -> Response:
        item = get_object_or_404(self.queryset, pk=pk)
        return Response(self.serializer_class(item).data)

    def destroy(self, request: Request, pk: int) -> Response:
        item = get_object_or_404(self.queryset, pk=pk)
        item.delete()
        return Response(
            {
                'message': f'{self.queryset.model.__name__} '
                           f'with id {pk} successfully deleted'
            },
            status=HTTP_200_OK)
