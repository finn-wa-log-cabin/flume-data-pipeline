from datetime import datetime

from main.common.domain.messages.summary import SummaryPeriod
from main.common.domain.tables.table_schema import TableSchema
from main.common.utils.time import timestamp
from marshmallow_dataclass import dataclass


@dataclass
class DeviceTelemetry(TableSchema):
    """The schema for the DeviceTelemetry table.
    Stores raw and average readings from devices.
    """

    customerID: str
    deviceID: str
    depth: int
    numReadings: int
    period: SummaryPeriod

    @classmethod
    def new(cls, timestamp_millis: str, **fields):
        """Creates a new DeviceTelemetry object, automatically generating values
        for PartitionKey & RowKey.

        Args:
        - timestamp_millis: Unix timestamp in millisecond precision. Represents
            the time the message was received. Used as RowKey.
        - fields: Values for class fields (excluding PartitionKey & RowKey).

        Returns: A new DeviceTelemetry object.
        """

        return cls(
            PartitionKey=cls.partition_key(
                fields["customerID"], fields["deviceID"], fields["period"]
            ),
            RowKey=str(timestamp_millis),
            **fields,
        )

    @staticmethod
    def partition_key(customerID: str, deviceID: str, period: SummaryPeriod) -> str:
        """Creates the partition key for a DeviceTelemetry row.

        Args:
        - customerID: The customer ID.
        - deviceID: The device ID.
        - period: The SummaryPeriod for the depth value.

        Returns: The partition key.
        """
        return f"{customerID}_{deviceID}_{period.name}"

    @staticmethod
    def row_key(dt: datetime) -> str:
        """Formats a datetime into a timestamp for use as a RowKey.

        Args:
        - dt: The datetime that the message was received.

        Returns: A Unix timestamp in millisecond precision.
        """
        return str(timestamp(dt))
