import pytz
from datetime import datetime

from api.client import client


async def fetch_restriction_time() -> str:
    async with client.get('lms/absence-time/') as response:
        data: list[dict[str, tp.Any]] = await response.json()
    return data['absence_restriction_time']


def utc_to_local(utc_dt: datetime) -> datetime:
    local_tz = pytz.timezone('Europe/Moscow')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


async def absence_report_overdue() -> bool:
    utc_now = datetime.utcnow()
    local_now = utc_to_local(utc_now).strftime('%H:%M:%S')
    restriction_time = await fetch_restriction_time()
    return restriction_time >= local_now
