from datetime import datetime

from marshmallow_dataclass import dataclass

from ...utils.time import timestamp
from .table_schema import TableSchema


@dataclass
class DeviceTelemetry(TableSchema):
    """The schema for the DeviceTelemetry table.
    Stores raw readings from devices.
    """

    customerID: str
    deviceID: str
    depth: int
    messageCount: int
    eventTimestamp: int

    @classmethod
    def new(
        cls, customerID: str, deviceID: str, depth: int, messageCount: int, eventTimestamp: int
    ):
        """Creates a new DeviceTelemetry object, automatically generating values
        for PartitionKey & RowKey.

        Args: Values for class fields (excluding PartitionKey & RowKey).

        Returns: A new DeviceTelemetry object.
        """

        return cls(
            PartitionKey=cls.partition_key(customerID, deviceID),
            RowKey=str(eventTimestamp),
            customerID=customerID,
            deviceID=deviceID,
            depth=depth,
            messageCount=messageCount,
            eventTimestamp=eventTimestamp,
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
        return str(timestamp(dt))
