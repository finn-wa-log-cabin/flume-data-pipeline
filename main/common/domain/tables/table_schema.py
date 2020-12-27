from main.common.domain.schema_type import SchemaType
from marshmallow_dataclass import dataclass


@dataclass
class TableSchema(SchemaType):
    """A schema for an Azure Table, containing a PartitionKey and a RowKey."""

    PartitionKey: str
    RowKey: str
