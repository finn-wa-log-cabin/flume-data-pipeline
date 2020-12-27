import logging
from typing import List

from dateutil import tz, utils
from main.common.domain.messages.summary import *
from main.common.domain.messages.timer_request import TimerRequest
from main.common.domain.tables.device import Device
from main.common.domain.tables.device_telemetry import DeviceTelemetry
from main.common.utils.time import *
from main.InsertTelemetry.insert_telemetry import RAW_TELEMETRY


def device_summary_req_msgs(timerJson: str, devicesJson: str, period: SummaryPeriod) -> str:
    """Generates a list of serialised DeviceSummaryRequests.
    This function can be used to fan out a single SummaryRequest.

    Args:
    - timerJson: Serialised TimerRequest which triggered the SummaryRequest
    - devicesJson: Serialized list of Devices which DeviceSummaryRequests should
        be created for
    - period: Period to summarise

    Returns: A list of serialised DeviceSummaryRequests.
    """
    timer: TimerRequest = TimerRequest.Schema().loads(timerJson)
    devices: List[Device] = Device.Schema(many=True).loads(devicesJson)

    if timer.IsPastDue:
        logging.warn(f"{period.name} timer is past due!")

    request = SummaryRequest(
        period=period,
        startTime=start_of_day(as_utc(timer.ScheduleStatus.Last)),
        endTime=start_of_day(utils.today(tz.UTC)),
    )

    schema = DeviceSummaryRequest.Schema(many=True)
    return schema.dumps([device_summmary_request(request, d) for d in devices])


def device_summmary_request(request: SummaryRequest, device: Device) -> DeviceSummaryRequest:
    return DeviceSummaryRequest(
        period=request.period,
        startTimestamp=timestamp(request.startTime),
        endTimestamp=timestamp(request.endTime),
        readPartition=DeviceTelemetry.partition_key(
            device.customerID, device.deviceID, RAW_TELEMETRY
        ),
        writePartition=DeviceTelemetry.partition_key(
            device.customerID, device.deviceID, request.period
        ),
        writeRow=DeviceTelemetry.row_key(request.endTime),
        device=device,
    )
