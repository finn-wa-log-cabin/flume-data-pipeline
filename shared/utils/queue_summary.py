import logging
from typing import List

from dateutil import tz, utils
from shared.domain.messages.summary_request import *
from shared.domain.messages.timer_request import TimerRequest
from shared.domain.tables.device import Device
from shared.domain.tables.device_telemetry import DeviceTelemetry
from shared.domain.tables.summary import Summary
from shared.utils.time import *


def device_summary_req_msgs(
    timerJson: str, devicesJson: str, timespan: SummaryTimespan
) -> str:
    """Generates a list of serialised DeviceSummaryRequests.
    This function can be used to fan out a single SummaryRequest.

    Args:
    - timerJson: Serialised TimerRequest which triggered the SummaryRequest
    - devicesJson: Serialized list of Devices which DeviceSummaryRequests should
        be created for
    - timespan: The timespan to bin data in before summarising

    Returns: A list of serialised DeviceSummaryRequests.
    """
    timer: TimerRequest = TimerRequest.Schema().loads(timerJson)
    devices: List[Device] = Device.Schema(many=True).loads(devicesJson)

    if timer.IsPastDue:
        logging.warn(f"{timespan.name} timer is past due!")

    request = SummaryRequest(
        timespan=timespan,
        startTime=start_of_day(as_utc(timer.ScheduleStatus.Last)),
        endTime=start_of_day(utils.today(tz.UTC)),
    )

    schema = DeviceSummaryRequest.Schema(many=True)
    return schema.dumps([device_summmary_request(request, d) for d in devices])


def device_summmary_request(
    request: SummaryRequest, device: Device
) -> DeviceSummaryRequest:
    return DeviceSummaryRequest(
        timespan=request.timespan,
        startTimestamp=timestamp(request.startTime),
        endTimestamp=timestamp(request.endTime),
        readPartition=DeviceTelemetry.partition_key(device.customerID, device.deviceID),
        writePartition=Summary.partition_key(
            device.customerID, device.deviceID, request.timespan
        ),
        device=device,
    )
