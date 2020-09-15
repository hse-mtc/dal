from django.db.models.query import QuerySet
from django.db.models import Value
from django.db.models.functions import (
    Lower,
    Concat,
)
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.decorators import action


class GetPutPostDeleteModelViewSet(ModelViewSet):
    query_params_serializer_class = None

    # get_by_id = True
    get_filters = []
    special_get_filters = []

    def list(self, request: Request) -> Response:
        items = self.queryset

        # check query params
        query_params = self.query_params_serializer_class(data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors,
                            status=HTTP_400_BAD_REQUEST)

        # get by id
        # if self.get_by_id and 'id' in request.query_params:
            # item = items.get(id=request.query_params['id'])
            # return Response(self.serializer_class(item).data)

        # filter by filters
        for filt in self.get_filters:
            if filt in request.query_params:
                items = items.filter(**{filt: request.query_params[filt]})
        
        # filter by special filters
        for filt in self.special_get_filters:
            if filt in request.query_params:
                items = self.special_get_filters[filt](items, request)

        return Response(self.serializer_class(items, many=True).data)

    def retrieve(self, request: Request, pk: int) -> Response:
        item = get_object_or_404(self.queryset, pk=pk)
        return Response(self.serializer_class(item).data)


def filter_names(items: QuerySet, request: Request) -> QuerySet:
    items = items.annotate(search_name=Lower(
        Concat('surname', Value(' '), 'name', Value(' '),
               'patronymic')))
    items = items.filter(
        search_name__contains=request.query_params['name'].lower())
    return items
