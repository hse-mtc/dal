from datetime import timedelta, datetime


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


def get_current_semester_range() -> tuple[datetime, datetime]:
    first_semester_months = list(range(9, 13))
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    if current_month in first_semester_months:
        return datetime(current_year, 9, 1), datetime(current_year, 12, 31)
    return datetime(current_year, 1, 1), datetime(current_year, 8, 31)
