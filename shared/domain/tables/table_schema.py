import json

from flatten_json import flatten, unflatten
from marshmallow_dataclass import dataclass
from shared.domain.schema_type import SchemaType


@dataclass
class TableSchema(SchemaType):
    """A schema for an Azure Table, containing a PartitionKey and a RowKey."""

    PartitionKey: str
    RowKey: str

    @classmethod
    def dumps_flattened(cls, data, many=False) -> str:
        """Returns a serialised JSON string of the object, flattened so that
        nested objects are included in the top level.
        e.g.
        ```json
        {
            "customerID": "TestCustomer",
            "sensorData.temperature": 19.7,
            // etc
        }
        ```

        Args:
        - data: The object or list of objects to serialise
        - many: Set to true if data is a list of objects

        Returns: JSON string of the current object
        """
        unflattened = cls.Schema().dump(data, many=many)
        if many:
            flattened = [flatten(obj) for obj in unflattened]
        else:
            flattened = flatten(unflattened)
        return json.dumps(flattened, sort_keys=True)

    @classmethod
    def loads_flattened(cls, flattened_str: str, many=False):
        """Deserialises an object from a flattened JSON string. The inverse of
        dumps_flattened().

        Args:
        - flattened_str: The serialised flattened JSON string
        - many: Set to true if the string is an array of objects

        Returns: a new object (or list of objects if many=True)
        """
        flattened = json.loads(flattened_str)
        if many:
            unflattened = [unflatten(obj) for obj in flattened]
        else:
            unflattened = unflatten(flattened)
        return cls.Schema().load(unflattened, many=many)
