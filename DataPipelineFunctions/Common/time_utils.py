from datetime import datetime
from dateutil import tz, utils


def timestamp(dt: datetime) -> int:
    """
    Returns the datetime as a Unix timestamp with millisecond precision.
    """
    return round(dt.timestamp() * 1000)


def as_utc(dt: datetime) -> datetime:
    """
    Returns the datetime object with a UTC timezone. Date and time data is
    adjusted so that the UTC timestamp remains the same.
    """
    dt = utils.default_tzinfo(dt, tz.UTC)
    return dt.astimezone(tz.UTC)


def start_of_day(dt: datetime) -> datetime:
    """
    Returns a datetime with the same day, month, year, and tzinfo values but
    with the time set to the start of the day.
    """
    return datetime(dt.year, dt.month, dt.day, tzinfo=dt.tzinfo)