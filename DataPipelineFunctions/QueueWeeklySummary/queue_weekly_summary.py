from typing import List

import azure.functions as func
from DataPipelineFunctions.Common.queue_summary import get_request_msgs
from DataPipelineFunctions.Common.summary import SummaryRequest


def main(timerJson: str, devicesJson: str, msgs: func.Out[List[str]]):
    request = SummaryRequest("Weekly", 7)
    msgs.set(get_request_msgs(timerJson, devicesJson, request))
