from typing import Dict, List

import pandas as pd
from pandas.core.frame import DataFrame
from shared.domain.messages.summary_request import DeviceSummaryRequest
from shared.domain.tables.device_telemetry import DeviceTelemetry, SensorData
from shared.domain.tables.summary import Summary
from shared.utils.time import timestamp


def main(requestMsg: str, dataJson: str) -> str:
    """Calculates averages for the data passed in, and returns a summary to be
    inserted into the DeviceTelemetry table.

    Args:
    - requestMsg: The serialised DeviceSummaryRequest
    - dataJson: The serialised list of DeviceTelemetry readings

    Returns: An array of serialised Summary rows
    """
    request: DeviceSummaryRequest = DeviceSummaryRequest.Schema().loads(requestMsg)
    telemetry: List[DeviceTelemetry] = DeviceTelemetry.loads_flattened(
        dataJson, many=True
    )
    dataframe = load_dataframe([t.sensorData for t in telemetry])
    binned_mean: List[Dict] = (
        dataframe.resample(request.timespan.value, label="left", closed="right")
        .mean()
        .reset_index()
        .to_dict(orient="records")
    )
    summaries = [create_summary(mean_data, request) for mean_data in binned_mean]
    return Summary.dumps_flattened(summaries, many=True)


def load_dataframe(sensor_data: List[SensorData]) -> DataFrame:
    df = DataFrame(sensor_data, columns=SensorData.Schema().fields.keys())
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    return df.set_index("timestamp")


def create_summary(mean_dict: dict, request: DeviceSummaryRequest) -> Summary:
    start_time = timestamp(mean_dict["timestamp"].to_pydatetime())
    mean_data = SensorData(
        timestamp=start_time,
        humidity=mean_dict["humidity"],
        temperature=mean_dict["temperature"],
    )
    return Summary.new(
        customerID=request.device.customerID,
        deviceID=request.device.deviceID,
        timespan=request.timespan,
        startTimestamp=start_time,
        meanData=mean_data,
    )
