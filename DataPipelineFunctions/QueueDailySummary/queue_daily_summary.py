from DataPipelineFunctions.Common.summary import SummaryRequest
from datetime import datetime
import logging
import json
import typing
from DataPipelineFunctions.Common.timer_request import TimerRequest


def main(timerJson: str, devicesJson: str) -> str:
    request = SummaryRequest("Daily", 1)
    logging.info(timerJson)
    timer = TimerRequest(timerJson)
    if timer.past_due:
        logging.warn("Daily summary timer is past due!")

    # Set start and end times to start of day
    last = timer.schedule_status.last
    request.set_start_time(datetime(last.year, last.month, last.day))
    now = datetime.now()
    request.set_end_time(datetime(now.year, now.month, now.day))

    devices = json.loads(devicesJson)
    return request.generate_messages(devices)
