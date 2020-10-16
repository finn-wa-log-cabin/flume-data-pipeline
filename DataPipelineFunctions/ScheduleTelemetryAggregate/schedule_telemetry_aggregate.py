from datetime import datetime, timedelta
import logging
import json
from ..Common.scheduling import TimerRequest


def main(timerJson: str, devicesJson: str) -> str:
    devices = json.loads(devicesJson)
    timer = TimerRequest(timerJson)
    if timer.past_due:
        logging.warn("Aggregate timer is past due!")
    logging.info(timerJson)

    # probably going to have to make a function for each aggregate interval
    # can use shared code for processing requests though

    # {
    #   "direction": "out",
    #   "type": "queue",
    #   "name": "$return",
    #   "queueName": "aggregate-requests",
    #   "connection": "AzureWebJobsStorage"
    # }
