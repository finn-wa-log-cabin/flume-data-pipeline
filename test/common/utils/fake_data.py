from datetime import datetime, timedelta
from random import randrange
from typing import List

from main.common.domain.tables.device_telemetry import DeviceTelemetry
from main.common.utils.time import timestamp

CUSTOMER_ID = "FakeCustomer1"
DEVICE_ID = "FakeDevice1"
START_TIME = datetime(2020, 1, 5)
END_TIME = datetime(2020, 3, 12)
START_DEPTH = 250
MIN_DEPTH = 0
MAX_DEPTH = 500

fake_data: List[DeviceTelemetry] = []
current_time = START_TIME
depth = START_DEPTH
message_count = 1
while current_time < END_TIME:
    fake_data.append(
        DeviceTelemetry.new(
            customerID=CUSTOMER_ID,
            deviceID=DEVICE_ID,
            depth=depth,
            messageCount=message_count,
            eventTimestamp=timestamp(current_time),
        )
    )
    depth += randrange(-5, 5)
    depth = min(MAX_DEPTH, max(depth, MIN_DEPTH))
    current_time += timedelta(hours=1, seconds=randrange(-3, 3))
    message_count += 1

with open("fake_data.json", "w+") as file:
    file.write(DeviceTelemetry.Schema().dumps(fake_data, many=True))
