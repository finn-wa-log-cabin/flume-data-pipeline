import logging
from typing import List

from main.common.domain.messages.raw_telemetry import RawTelemetryMsg
from main.common.domain.messages.summary import DeviceSummaryRequest
from main.common.domain.tables.device_telemetry import DeviceTelemetry


def main(requestMsg: str, dataJson: str) -> str:
    """Calculates averages for the data passed in, and returns a summary to be
    inserted into the DeviceTelemetry table.

    Args:
    - requestMsg: The serialised DeviceSummaryRequest
    - dataJson: The serialised list of raw telemetry readings

    Returns: A single serialised DeviceTelemetry row as a summary
    """
    request: DeviceSummaryRequest = DeviceSummaryRequest.Schema().loads(requestMsg)
    data: List[RawTelemetryMsg] = RawTelemetryMsg.Schema(many=True).loads(dataJson)

    depth_readings = [d.depth for d in data]
    if len(depth_readings) == 0:
        logging.warn(f"No valid readings for summary request {requestMsg}")
    elif len(depth_readings) != len(data):
        logging.warn(f"Discarded invalid readings from {data} to produce {depth_readings}")
    else:
        summary = DeviceTelemetry(
            PartitionKey=request.writePartition,
            RowKey=request.writeRow,
            deviceID=request.device.deviceID,
            customerID=request.device.customerID,
            depth=sum(depth_readings) / len(depth_readings),
            period=request.period,
            numReadings=len(depth_readings),
        )
        return DeviceTelemetry.Schema().dumps(summary)
