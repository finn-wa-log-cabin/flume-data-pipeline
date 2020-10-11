from ..Common.telemetry_message import TelemetryMessage

import json
import logging
from datetime import datetime

import azure.functions as func


def main(event: func.EventGridEvent) -> str:
    """
    Receives telemetry from a device, and inserts the data into a table.
    """
    msg = TelemetryMessage(event.get_json())
    if msg.depth is None:
        logging.warn("Received depth of None %s", msg)

    return json.dumps(
        {
            "PartitionKey": msg.get_partition_raw(),
            "RowKey": str(datetime.utcnow().timestamp()),
            "depth": msg.depth,
            "messageId": msg.messageId,
        }
    )
