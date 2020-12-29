from base64 import b64decode

from azure.functions import EventGridEvent

from ..common.domain.messages.telemetry_msg import TelemetryMsg
from ..common.domain.tables.device_telemetry import *

RAW_TELEMETRY = SummaryPeriod("Raw", 0)


def main(event: EventGridEvent) -> str:
    """Receives telemetry from a device, and creates a table row for it.

    Args:
    - event: The event containing the device telemetry.

    Returns: The serialised row to be inserted into the DeviceTelemetry table.
    """
    body = b64decode(event.get_json()["body"])
    message: TelemetryMsg = TelemetryMsg.Schema().loads(body)
    row = DeviceTelemetry.new(
        str(message.timestamp),
        customerID=message.customerID,
        deviceID=message.deviceID,
        depth=message.depth,
        numReadings=1,
        period=RAW_TELEMETRY,
    )
    return DeviceTelemetry.Schema().dumps(row)
