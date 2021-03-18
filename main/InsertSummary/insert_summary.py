import pandas as pd
from main.common.domain.tables.summary import Summary
from pandas.core.frame import DataFrame

from ..common.domain.messages.summary_request import DeviceSummaryRequest


def main(requestMsg: str, dataJson: str) -> str:
    """Calculates averages for the data passed in, and returns a summary to be
    inserted into the DeviceTelemetry table.

    Args:
    - requestMsg: The serialised DeviceSummaryRequest
    - dataJson: The serialised list of DeviceTelemetry readings

    Returns: An array of serialised Summary rows
    """
    request: DeviceSummaryRequest = DeviceSummaryRequest.Schema().loads(requestMsg)
    data: DataFrame = pd.read_json(
        dataJson,
        typ="frame",
        orient="records",
        convert_dates=["eventTimestamp"],
        date_unit="ms",
    ).set_index("eventTimestamp")

    binned_averages = data["depth"].resample(request.timespan.value, label="left").mean()
    summaries = [
        create_summary(start_time, depth, request) for start_time, depth in binned_averages.items()
    ]
    return Summary.Schema().dumps(summaries, many=True)


def create_summary(
    start_time: pd.Timestamp, depth: float, request: DeviceSummaryRequest
) -> Summary:
    return Summary.new(
        **{
            "customerID": request.device.customerID,
            "deviceID": request.device.deviceID,
            "timespan": request.timespan,
            "startTime": start_time.to_pydatetime(),
            "meanDepth": depth,
        }
    )
