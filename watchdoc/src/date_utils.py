from datetime import datetime


def date_to_russian_format(date: datetime) -> str:
    return date.strftime("%d.%m.%Y")


def month_to_russian_title(month: int) -> str:
    return [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ][month - 1]


def today() -> datetime:
    return datetime.today()
