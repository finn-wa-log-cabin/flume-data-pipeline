from datetime import datetime
from main.common.domain.tables.summary import Summary
import pandas as pd

from pandas.core.frame import DataFrame
from ..common.domain.messages.summary import DeviceSummaryRequest
from ..common.domain.tables.device_telemetry import DeviceTelemetry


def main(requestMsg: str, dataJson: str) -> str:
    """Calculates averages for the data passed in, and returns a summary to be
    inserted into the DeviceTelemetry table.

    Args:
    - requestMsg: The serialised DeviceSummaryRequest
    - dataJson: The serialised list of DeviceTelemetry readings

    Returns: An array of serialised Summary rows
    """
    summary_req = DeviceSummaryRequest.Schema().loads(requestMsg)
    data: DataFrame = pd.read_json(
        dataJson,
        typ="frame",
        orient="records",
        convert_dates=["eventTimestamp"],
        date_unit="ms",
    ).set_index("eventTimestamp")

    binned_averages = data["depth"].resample("W-MON").mean()
    summaries = [
        create_summary(timestamp, depth, summary_req)
        for timestamp, depth in binned_averages.items()
    ]
    return Summary.Schema().dumps(summaries, many=True)


def create_summary(timestamp: datetime, depth: float, request: DeviceSummaryRequest) -> Summary:
    return {}  # TODO implement
