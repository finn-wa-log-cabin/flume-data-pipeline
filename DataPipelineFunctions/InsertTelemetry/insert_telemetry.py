import json
import logging
from datetime import datetime

from azure.functions import EventGridEvent
from ..Common.telemetry_message import TelemetryMessage


def main(telemetry: EventGridEvent) -> str:
    """
    Receives telemetry from a device, and inserts the data into a table.
    """
    msg = TelemetryMessage(telemetry.get_json())
    if msg.depth is None:
        logging.warn("Received depth of None %s", msg)

    event_time = telemetry.event_time()
    if event_time is None:
        event_time = datetime.now()
    event_millis = int(event_time.timestamp() * 1000)

    return json.dumps(
        {
            "PartitionKey": msg.get_partition_raw(),
            "RowKey": str(event_millis),
            "deviceID": msg.device_id,
            "depth": msg.depth,
            "messageID": msg.message_id,
        }
    )
