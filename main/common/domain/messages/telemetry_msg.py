from ....common.domain.schema_type import SchemaType
from marshmallow_dataclass import dataclass


@dataclass
class TelemetryMsg(SchemaType):
    """The JSON telemetry message received from a device."""

    customerID: str
    deviceID: str
    depth: int
    messageCount: int
    timestamp: int