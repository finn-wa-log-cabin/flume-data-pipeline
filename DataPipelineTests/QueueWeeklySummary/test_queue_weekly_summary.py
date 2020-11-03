import json
from datetime import datetime, timedelta

import DataPipelineFunctions.QueueWeeklySummary.queue_weekly_summary as qws
from DataPipelineFunctions.Common.time_utils import as_utc, start_of_day, timestamp
from dateutil import tz, utils
from dateutil.tz.tz import tzoffset

SAMPLES_PATH = "DataPipelineTests/QueueWeeklySummary/samples/"


def get_sample(name: str) -> str:
    with open(f"{SAMPLES_PATH}{name}.json", "r") as json_file:
        return json_file.read()


def test_queue_weekly_summary():
    timer_json = get_sample("timer")
    devices_json = get_sample("devices")
    nzdt = tzoffset("NZDT", timedelta(hours=13))
    expected = {
        "periodName": "Weekly",
        "periodDays": 7,
        "startTime": timestamp(start_of_day(as_utc(datetime(2020, 10, 19, tzinfo=nzdt)))),
        "endTime": timestamp(utils.today(tzinfo=tz.UTC)),
    }

    requests = json.loads(qws.main(timer_json, devices_json))
    devices = json.loads(devices_json)
    for i in range(len(requests)):
        req = requests[i]
        assert req["periodName"] == expected["periodName"]
        assert req["periodDays"] == expected["periodDays"]
        assert req["startTime"] == expected["startTime"]
        assert req["endTime"] == expected["endTime"]
        d = devices[i]
        assert req["device"] == d
        assert req["partitionKey"] == f"{d['customerID']}_{d['deviceID']}_Raw"