from datetime import datetime
from typing import Any, Dict

import shared.utils.time as time_utils
from marshmallow_dataclass import dataclass
from shared.domain.schema_type import SchemaType
from shared.domain.tables.table_schema import TableSchema


@dataclass
class SensorData(SchemaType):
    """The readings from the device sensors."""

    humidity: float
    temperature: float
    timestamp: int


@dataclass
class DeviceTelemetry(TableSchema):
    """The schema for the DeviceTelemetry table.
    Stores raw readings from devices.
    """

    customerID: str
    deviceID: str
    sensorData: SensorData
    messageCount: int
    insertTimestamp: int

    @classmethod
    def new(
        cls,
        customerID: str,
        deviceID: str,
        messageCount: int,
        sensorData: Dict[str, Any],
    ):
        """Creates a new DeviceTelemetry object, automatically generating values
        for PartitionKey & RowKey.

        Args: Values for class fields (excluding PartitionKey & RowKey).

        Returns: A new DeviceTelemetry object.
        """
        sensor_data = SensorData(**sensorData)
        return cls(
            PartitionKey=cls.partition_key(customerID, deviceID),
            RowKey=str(sensor_data.timestamp),
            customerID=customerID,
            deviceID=deviceID,
            sensorData=sensor_data,
            messageCount=messageCount,
            insertTimestamp=time_utils.timestamp(datetime.utcnow()),
        )

    @staticmethod
    def partition_key(customerID: str, deviceID: str) -> str:
        """Creates the partition key for a DeviceTelemetry row.

        Args:
        - customerID: The customer ID.
        - deviceID: The device ID.

        Returns: The partition key.
        """
        return f"{customerID}_{deviceID}"

    @staticmethod
    def row_key(dt: datetime) -> str:
        """Formats a datetime into a timestamp for use as a RowKey.

        Args:
        - dt: The datetime that the message was received.

        Returns: A Unix timestamp in millisecond precision.
        """
        return str(time_utils.timestamp(dt))
