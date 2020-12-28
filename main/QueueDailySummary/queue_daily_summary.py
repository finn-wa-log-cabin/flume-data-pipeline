from ..common.domain.messages.summary import SummaryPeriod
from ..common.utils.summary import device_summary_req_msgs

DAILY_PERIOD = SummaryPeriod("Daily", 1)


def main(timerJson: str, devicesJson: str) -> str:
    """This function is triggered on a daily basis by a timer. It requests a
    summary for all telemetry collected over the last day, for each device.

    Args:
    - timerJson: The serialised timer trigger
    - devicesJson: The serialised list of all devices

    Returns: A list of serialised DeviceSummaryRequests
    """
    return device_summary_req_msgs(timerJson, devicesJson, DAILY_PERIOD)
