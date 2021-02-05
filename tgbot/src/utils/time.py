import pytz
from datetime import datetime

CHECK_TIME = '09:15'

def check_time() -> bool:
    utc_now = datetime.utcnow()
    local_now = utc_to_local(utc_now).strftime('%H:%M')
    return CHECK_TIME >= local_now


def utc_to_local(utc_dt: datetime) -> datetime:
    local_tz = pytz.timezone('Europe/Moscow')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)
