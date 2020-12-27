from datetime import datetime

from ....common.domain.schema_type import SchemaType
from ....common.domain.tables.device import Device
from marshmallow_dataclass import dataclass


@dataclass
class SummaryPeriod(SchemaType):
    """A period of time for a summary."""

    name: str
    days: int


@dataclass
class SummaryRequest(SchemaType):
    """A request for a summary.
    A summary contains the average depth reading for a device over a given
    period. It is inserted into the DeviceTelemetry table.
    """

    period: SummaryPeriod
    startTime: datetime
    endTime: datetime


@dataclass
class DeviceSummaryRequest(SchemaType):
    """A summary request for a specific device.
    Contains parameter values used by the Function to collect the raw data to
    summarise.
    """

    period: SummaryPeriod
    device: Device
    startTimestamp: int
    endTimestamp: int
    readPartition: str
    writePartition: str
    writeRow: int
