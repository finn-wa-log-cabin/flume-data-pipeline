from ..common.domain.messages.summary import SummaryPeriod
from ..common.utils.summary import device_summary_req_msgs

WEEKLY_PERIOD = SummaryPeriod("Weekly", 7)


def main(timerJson: str, devicesJson: str):
    """This function is triggered on a weekly basis by a timer. It requests a
    summary for all telemetry collected over the last week, for each device.

    Args:
    - timerJson: The serialised timer trigger
    - devicesJson: The serialised list of all devices

    Returns: A list of serialised DeviceSummaryRequests
    """
    return device_summary_req_msgs(timerJson, devicesJson, WEEKLY_PERIOD)
