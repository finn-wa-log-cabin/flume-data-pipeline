from marshmallow_dataclass import dataclass
from shared.domain.schema_type import SchemaType


@dataclass
class TableSchema(SchemaType):
    """A schema for an Azure Table, containing a PartitionKey and a RowKey."""

    PartitionKey: str
    RowKey: str
