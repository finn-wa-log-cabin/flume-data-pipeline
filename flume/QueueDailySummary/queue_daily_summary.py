from cabin.domain.summary_timespan import SummaryTimespan
from cabin.utils.queue_summary import device_summary_req_msgs


def main(timerJson: str, devicesJson: str) -> str:
    """This function is triggered on a daily basis by a timer. It requests a
    summary for all telemetry collected over the last day, for each device.

    Args:
    - timerJson: The serialised timer trigger
    - devicesJson: The serialised list of all devices

    Returns: A list of serialised DeviceSummaryRequests
    """
    return device_summary_req_msgs(timerJson, devicesJson, SummaryTimespan.DAILY)
