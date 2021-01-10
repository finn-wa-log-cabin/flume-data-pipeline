from datetime import datetime

from ....common.domain.messages.summary import SummaryPeriod
from ....common.domain.tables.table_schema import TableSchema
from ....common.utils.time import dateint
from marshmallow_dataclass import dataclass


@dataclass
class Summary(TableSchema):
    """The schema for the Summary table.
    Stores aggregate telemetry data.
    """

    customerID: str
    deviceID: str
    startTime: datetime
    endTime: datetime
    period: SummaryPeriod
    meanDepth: float
    numReadings: int

    @classmethod
    def new(cls, **fields):
        """Creates a new DeviceTelemetry object, automatically generating values
        for PartitionKey & RowKey.

        Args:
        - fields: Values for class fields (excluding PartitionKey & RowKey).

        Returns: A new DeviceTelemetry object.
        """

        return cls(
            PartitionKey=cls.partition_key(
                fields["customerID"], fields["deviceID"], fields["period"]
            ),
            RowKey=fields["startTime"],
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
    def row_key(start_time: datetime) -> str:
        """Formats a datetime into a dateint for use as a RowKey.

        Args:
        - dt: The datetime that the message was received.

        Returns: A dateint as a string (format YYYYMMDD)
        """
        return str(dateint(start_time))
