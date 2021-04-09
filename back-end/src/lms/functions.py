from datetime import timedelta, datetime

from django.db.models import Model
from django.db.models import Q

from rest_framework.serializers import Serializer


def get_date_range(date_from: datetime, date_to: datetime,
                   weekday: int) -> list[str]:
    """
    Calculate dates with the same weekday from the date range provided

    :param date_from: starting date range
    :param date_to: ending date range
    :param weekday: weekday number [0;6]  (0-Monday)
    :return: array of dates
    """
    start_date = date_from + timedelta((weekday - date_from.weekday() + 7) % 7)

    dates = []
    cur_date = start_date

    while cur_date <= date_to:
        dates.append(cur_date.strftime('%Y-%m-%d'))
        cur_date += timedelta(7)

    return dates


def search_persons(model: Model, serializer: Serializer,
                   field: str) -> list[dict]:
    return serializer(model.objects.filter(
        Q(name__icontains=field) | Q(surname__icontains=field) |
        Q(patronymic__icontains=field)),
                      many=True)


def persons_response(data: list[dict]) -> list[dict]:
    result = []
    for item in data.data:
        res = {
            'id': item.get('user', 1),  # TODO: fix
            'fullname': item.get('fullname', None)
        }
        result.append(res)
    return result
