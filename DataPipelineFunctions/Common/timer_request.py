import json
from datetime import datetime
from dateutil import parser


class ScheduleStatus:
    """
    Represents a timer schedule status. This isn't currently in the Python SDK
    (see: https://github.com/Azure/azure-functions-python-worker/issues/681) but
    it is in the raw JSON.

    - last: Last recorded schedule occurrence
    - next: Expected next schedule occurrence
    - last_updated: The last time this record was updated. This is used to
      re-calculate Next with the current Schedule after a host restart.
    """

    last: datetime
    next: datetime
    last_updated: datetime

    def __init__(self, raw_dict: dict):
        self.last = parser.isoparse(raw_dict["Last"])
        self.next = parser.isoparse(raw_dict["Next"])
        self.last_updated = parser.isoparse(raw_dict["LastUpdated"])


class TimerRequest:
    """
    A more complete version of the TimerRequest - see ScheduleStatus
    """

    schedule_status: ScheduleStatus
    past_due: bool

    def __init__(self, raw_json: str):
        raw_dict = json.loads(raw_json)
        self.schedule_status = ScheduleStatus(raw_dict["ScheduleStatus"])
        self.past_due = raw_dict["IsPastDue"]