import json
from datetime import datetime
import logging
from typing import List

from DataPipelineFunctions.Common.time_utils import dateint, timestamp


class SummaryRequest:
    name: str
    period_days: int
    start_time: datetime
    end_time: datetime

    def __init__(self, name: str, period_days: int):
        self.name = name
        self.period_days = period_days

    def set_start_time(self, start: datetime):
        self.start_time = start

    def set_end_time(self, end: datetime):
        self.end_time = end

    def get_queue_output(self, devices: List[dict]) -> str:
        return json.dumps([self.get_message(d) for d in devices])

    def get_message(self, device: dict) -> dict:
        partition_prefix = f"{device['customerID']}_{device['deviceID']}_"
        return {
            "readPartition": partition_prefix + "Raw",
            "writePartition": partition_prefix + self.name,
            "writeRow": dateint(self.end_time),
            "startTime": timestamp(self.start_time),
            "endTime": timestamp(self.end_time),
            "device": device,
            "periodName": self.name,
            "periodDays": self.period_days,
        }
