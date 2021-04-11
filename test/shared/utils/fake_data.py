from datetime import datetime, timedelta
from random import randrange
from typing import List

from shared.domain.tables.device_telemetry import DeviceTelemetry, SensorData
from shared.utils.time import timestamp

CUSTOMER_ID = "FakeCustomer1"
DEVICE_ID = "FakeDevice1"
VERSION = "1.0.0"

START_TIMESTAMP = timestamp(datetime(2020, 1, 5))
END_TIMESTAMP = timestamp(datetime(2020, 3, 12))

START_HUMIDITY = 65
MIN_HUMIDITY = 0
MAX_HUMIDITY = 100

START_TEMP = 20.0
MIN_TEMP = 5.0
MAX_TEMP = 30.0

START_MSG_COUNT = 1


def fake_data():
    generated: List[DeviceTelemetry] = []
    telemetry = init_telemetry()
    while telemetry.sensorData.timestamp < END_TIMESTAMP:
        generated.append(telemetry)
        telemetry = next_telemetry(telemetry)

    with open("fake_data.json", "w+") as file:
        file.write(DeviceTelemetry.Schema().dumps(generated, many=True))


def init_telemetry() -> DeviceTelemetry:
    next_data = SensorData(
        timestamp=START_TIMESTAMP, humidity=START_HUMIDITY, temperature=START_TEMP
    )
    return DeviceTelemetry.new(
        customerID=CUSTOMER_ID,
        deviceID=DEVICE_ID,
        sensorData={
            "timestamp": START_TIMESTAMP,
            "humidity": START_HUMIDITY,
            "temperature": START_TEMP,
        },
        messageCount=START_MSG_COUNT,
        version=VERSION,
    )


def next_timestamp(ts: int) -> int:
    return ts + int(timedelta(hours=1, seconds=randrange(-3, 3)).total_seconds())


def next_humidity(humidity: float) -> float:
    humidity += randrange(-5, 5)
    return round(min(MAX_HUMIDITY, max(humidity, MIN_HUMIDITY)))


def next_temp(temp: float) -> float:
    temp += float(randrange(-3, 3)) / 10
    return round(min(MAX_TEMP, max(temp, MIN_TEMP)), 2)


def next_msg_count(msg_count: int) -> int:
    return msg_count + 1


def next_telemetry(telemetry: DeviceTelemetry) -> DeviceTelemetry:
    return DeviceTelemetry.new(
        customerID=CUSTOMER_ID,
        deviceID=DEVICE_ID,
        sensorData={
            "humidity": next_humidity(telemetry.sensorData.humidity),
            "temperature": next_temp(telemetry.sensorData.temperature),
            "timestamp": next_timestamp(telemetry.sensorData.timestamp),
        },
        messageCount=next_msg_count(telemetry.messageCount),
        version=VERSION,
    )


if __name__ == "__main__":
    fake_data()
