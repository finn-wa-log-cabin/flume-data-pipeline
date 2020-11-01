import json
from datetime import datetime
import logging
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

    def get_queue_output(self, devices: List[dict]) -> str:
        return json.dumps([self.get_message(d) for d in devices])

    def get_message(self, device: dict) -> dict:
        partitionKey = f"{device['customerID']}_{device['deviceID']}_Raw"
        logging.info(partitionKey)
        return {
            "partition": partitionKey,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "device": device,
            "periodName": self.name,
            "periodDays": self.period_days,
        }
