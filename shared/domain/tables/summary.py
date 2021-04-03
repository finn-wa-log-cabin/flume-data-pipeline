from datetime import datetime

from marshmallow_dataclass import dataclass
from shared.domain.summary_timespan import SummaryTimespan
from shared.domain.tables.device_telemetry import SensorData
from shared.domain.tables.table_schema import TableSchema
from shared.utils.time import dateint, timestamp


@dataclass
class Summary(TableSchema):
    """The schema for the Summary table.
    Stores aggregate telemetry data.
    """

    customerID: str
    deviceID: str
    timespan: SummaryTimespan
    startTimestamp: int
    meanData: SensorData

    @classmethod
    def new(
        cls,
        customerID: str,
        deviceID: str,
        timespan: SummaryTimespan,
        startTimestamp: int,
        meanData: SensorData,
    ):
        """Creates a new Summary object, automatically generating values
        for PartitionKey & RowKey.

        Args: Values for class fields (excluding PartitionKey & RowKey).

        Returns: A new Summary object.
        """
        return cls(
            PartitionKey=cls.partition_key(customerID, deviceID, timespan),
            RowKey=str(startTimestamp),
            customerID=customerID,
            deviceID=deviceID,
            timespan=timespan,
            startTimestamp=startTimestamp,
            meanData=meanData,
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
        """Formats a datetime into a timestamp for use as a RowKey.

        Args:
        - dt: The datetime that the message was received.

        Returns: A timestamp as a string
        """
        return str(timestamp(start_time))
