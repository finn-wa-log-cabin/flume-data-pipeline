from ....common.domain.schema_type import SchemaType
from marshmallow_dataclass import dataclass


@dataclass
class RawTelemetryMsg(SchemaType):
    """The JSON telemetry message received from a device."""

    customerID: str
    deviceID: str
    depth: int
    messageCount: int
    # include timestamp?? for delayed messages?? it does connect to a time server
