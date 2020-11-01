import logging
from DataPipelineFunctions.Common.queue_summary import get_request_msgs
from DataPipelineFunctions.Common.summary import SummaryRequest

DAILY_SUMMARY_REQUEST = SummaryRequest("Daily", 1)


def main(timerJson: str, devicesJson: str) -> str:
    msgs = get_request_msgs(timerJson, devicesJson, DAILY_SUMMARY_REQUEST)
    logging.info(msgs)
    return msgs
