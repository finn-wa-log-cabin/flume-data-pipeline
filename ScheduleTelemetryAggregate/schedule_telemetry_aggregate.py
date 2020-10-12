from datetime import datetime, timedelta
import logging

from common.scheduling import TimerRequest


def main(request: str) -> str:
    timer = TimerRequest(request)

    if timer.past_due:
        logging.warn("Aggregate timer is past due!")
