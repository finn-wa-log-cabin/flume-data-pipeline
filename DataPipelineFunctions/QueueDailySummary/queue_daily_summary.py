from DataPipelineFunctions.Common.queue_summary import get_request_msgs
from DataPipelineFunctions.Common.summary import SummaryRequest

DAILY_SUMMARY_REQUEST = SummaryRequest("Daily", 1)


def main(timerJson: str, devicesJson: str) -> str:
    return get_request_msgs(timerJson, devicesJson, DAILY_SUMMARY_REQUEST)
