import json
import logging
from typing import List

from DataPipelineFunctions.Common.summary import SummaryRequest
from DataPipelineFunctions.Common.time_utils import as_utc, start_of_day
from DataPipelineFunctions.Common.timer_request import TimerRequest
from dateutil import tz, utils


def get_request_msgs(timerJson: str, devicesJson: str, summary_req: SummaryRequest) -> List[str]:
    """
    Common code for queueing summaries
    """
    timer = TimerRequest(timerJson)
    if timer.past_due:
        logging.warn(f"{summary_req.name} timer is past due!")

    summary_req.set_start_time(start_of_day(as_utc(timer.schedule_status.last)))
    summary_req.set_end_time(start_of_day(utils.today(tz.UTC)))

    devices = json.loads(devicesJson)
    return summary_req.get_queue_output(devices)
