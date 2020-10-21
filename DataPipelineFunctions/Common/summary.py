import json
from datetime import datetime
from typing import List

from DataPipelineFunctions.Common.time_utils import timestamp


class SummaryRequest:
    name: str
    period_days: int
    start_time: int
    end_time: int

    def __init__(self, name: str, period_days: int):
        self.name = name
        self.period_days = period_days

    def set_start_time(self, start: datetime):
        self.start_time = timestamp(start)

    def set_end_time(self, end: datetime):
        self.end_time = timestamp(end)

    def generate_messages(self, devices: List[dict]) -> str:
        msg = {
            "periodName": self.name,
            "periodDays": self.period_days,
            "startTime": self.start_time,
            "endTime": self.end_time,
        }
        return [json.dumps({"device": d, **msg}) for d in devices]
