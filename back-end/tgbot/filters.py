from django_filters.rest_framework import FilterSet

from tgbot.models import Session


class SessionFilter(FilterSet):

    class Meta:
        model = Session
        fields = '__all__'
