from datetime import datetime


def to_timestamp(time: datetime) -> int:
    return int(time.timestamp() * 1000)