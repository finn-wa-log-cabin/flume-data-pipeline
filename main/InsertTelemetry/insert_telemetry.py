from base64 import b64decode
import json
from azure.functions import EventGridEvent

from ..common.domain.tables.device_telemetry import DeviceTelemetry


def main(event: EventGridEvent) -> str:
    """Receives telemetry from a device, and creates a table row for it.

    Args:
    - event: The event containing the device telemetry.

    Returns: The serialised row to be inserted into the DeviceTelemetry table.
    """
    body = json.loads(b64decode(event.get_json()["body"]))
    row = DeviceTelemetry.new(**body)
    return DeviceTelemetry.Schema().dumps(row)
