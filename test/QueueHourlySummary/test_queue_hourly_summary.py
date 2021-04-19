import json
from datetime import datetime

from dateutil import tz
from shared.utils.files import *
from shared.utils.time import *

from QueueHourlySummary import queue_hourly_summary as qhs

SAMPLES_PATH = "test/QueueHourlySummary/samples/"


def test_queue_hourly_summary():
    timer_json = load_text(SAMPLES_PATH + "timer.json")
    devices_json = load_text(SAMPLES_PATH + "devices.json")
    nzdt = tz.gettz("Pacific/Auckland")
    expected_start = as_utc(datetime(2020, 10, 19, 12, tzinfo=nzdt))
    expected_end = as_utc(
        datetime.now(tz=nzdt).replace(minute=0, second=0, microsecond=0)
    )

    requests = json.loads(qhs.main(timer_json, devices_json))
    devices = json.loads(devices_json)
    for i in range(len(requests)):
        req = requests[i]
        assert req["timespan"] == "HOURLY"
        assert fromtimestamp(req["startTimestamp"]) == expected_start
        assert fromtimestamp(req["endTimestamp"]) == expected_end
        d = devices[i]
        assert req["device"] == d
        assert req["readPartition"] == f"{d['customerID']}_{d['deviceID']}"
        assert req["writePartition"] == f"{d['customerID']}_{d['deviceID']}_HOURLY"
