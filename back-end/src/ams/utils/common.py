from datetime import datetime


def get_current_admission_year():
    now = datetime.now()
    if (now.month, now.day) >= (9, 1):
        return now.year + 1
    return now.year
