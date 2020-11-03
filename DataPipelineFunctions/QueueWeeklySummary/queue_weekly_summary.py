from DataPipelineFunctions.Common.queue_summary import get_request_msgs
from DataPipelineFunctions.Common.summary import SummaryRequest

WEEKLY_SUMMARY_REQUEST = SummaryRequest("Weekly", 7)


def main(timerJson: str, devicesJson: str) -> str:
    return get_request_msgs(timerJson, devicesJson, WEEKLY_SUMMARY_REQUEST)
