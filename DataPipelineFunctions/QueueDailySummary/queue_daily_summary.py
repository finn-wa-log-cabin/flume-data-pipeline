from DataPipelineFunctions.Common.time_utils import as_utc, start_of_day
import json
import logging
from datetime import datetime
from typing import List

import azure.functions as func
from DataPipelineFunctions.Common.summary import SummaryRequest
from DataPipelineFunctions.Common.timer_request import TimerRequest
from dateutil import tz, utils


def main(timerJson: str, devicesJson: str, requests: func.Out[List[str]]):
    request = SummaryRequest("Daily", 1)
    timer = TimerRequest(timerJson)
    if timer.past_due:
        logging.warn("Daily summary timer is past due!")
    # Set start and end times to start of day
    request.set_start_time(start_of_day(as_utc(timer.schedule_status.last)))
    request.set_end_time(start_of_day(as_utc(datetime.utcnow())))

    devices = json.loads(devicesJson)
    requests.set(request.generate_messages(devices))
