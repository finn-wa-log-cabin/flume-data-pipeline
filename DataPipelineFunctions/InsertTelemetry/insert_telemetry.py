import json
import logging
from datetime import datetime

from azure.functions import EventGridEvent


def main(event: EventGridEvent) -> str:
    """
    Receives telemetry from a device, and inserts the data into a table.
    """
    event_time = event.event_time()
    if event_time is None:
        event_time = datetime.now()
    event_millis = int(event_time.timestamp() * 1000)

    telemetry = json.loads(event.get_json())
    if telemetry["depth"] is None:
        raise TypeError(f"Received telemetry with null depth: {event}")
    telemetry["PartitionKey"] = telemetry["deviceID"] + "_Raw"
    telemetry["RowKey"] = str(event_millis)

    return json.dumps(telemetry)
