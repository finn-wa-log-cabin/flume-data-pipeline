from datetime import datetime

from marshmallow_dataclass import dataclass

from ...utils.time import dateint, timestamp
from ..summary_timespan import SummaryTimespan
from .table_schema import TableSchema


@dataclass
class Summary(TableSchema):
    """The schema for the Summary table.
    Stores aggregate telemetry data.
    """

    customerID: str
    deviceID: str
    timespan: SummaryTimespan
    startTimestamp: int
    meanDepth: float

    @classmethod
    def new(
        cls,
        start_time: datetime,
        customerID: str,
        deviceID: str,
        timespan: SummaryTimespan,
        meanDepth: float,
    ):
        """Creates a new Summary object, automatically generating values
        for PartitionKey & RowKey.

        Args: Values for class fields (excluding PartitionKey & RowKey).

        Returns: A new Summary object.
        """
        return cls(
            PartitionKey=cls.partition_key(customerID, deviceID, timespan),
            RowKey=cls.row_key(start_time),
            customerID=customerID,
            deviceID=deviceID,
            timespan=timespan,
            startTimestamp=timestamp(start_time),
            meanDepth=meanDepth,
        )

    @staticmethod
    def partition_key(customerID: str, deviceID: str, timespan: SummaryTimespan) -> str:
        """Creates the partition key for a Summary row.

        Args:
        - customerID: The customer ID.
        - deviceID: The device ID.
        - timespan: The timespan that this summary covers.

        Returns: The partition key.
        """
        return f"{customerID}_{deviceID}_{timespan.name}"

    @staticmethod
    def row_key(start_time: datetime) -> str:
        """Formats a datetime into a dateint for use as a RowKey.

        Args:
        - dt: The datetime that the message was received.

        Returns: A dateint as a string (format YYYYMMDD)
        """
        return str(dateint(start_time))
