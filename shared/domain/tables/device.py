from marshmallow_dataclass import dataclass
from shared.domain.tables.table_schema import TableSchema


@dataclass
class Device(TableSchema):
    """The schema for the Device table.
    Stores information about devices, their owners, and their water tank.
    """

    customerID: str
    deviceID: str

    @classmethod
    def new(cls, customerID: str, deviceID: str):
        """Creates a new Device object, automatically generating values for
        PartitionKey & RowKey.

        Args:
        - customerID: The customer ID. Also used as the PartitionKey.
        - deviceID: The device ID. Also used as the RowKey.

        Returns: A new Device object.
        """
        return cls(
            PartitionKey=customerID,
            RowKey=deviceID,
            customerID=customerID,
            deviceID=deviceID,
        )
