import json
from datetime import datetime, timedelta

from dateutil import tz, utils
from dateutil.tz.tz import tzoffset
from shared.utils.files import *
from shared.utils.time import as_utc, start_of_day, timestamp

from QueueHourlySummary import queue_hourly_summary as qhs

SAMPLES_PATH = "test/QueueHourlySummary/samples/"


def test_queue_hourly_summary():
    timer_json = load_text(SAMPLES_PATH + "timer.json")
    devices_json = load_text(SAMPLES_PATH + "devices.json")
    nzdt = tzoffset("NZDT", timedelta(hours=13))
    expected_start = timestamp(datetime(2020, 10, 19, 12, tzinfo=nzdt))
    expected_end = timestamp(
        datetime.now(tz=nzdt).replace(minute=0, second=0, microsecond=0)
    )

    requests = json.loads(qhs.main(timer_json, devices_json))
    devices = json.loads(devices_json)
    for i in range(len(requests)):
        req = requests[i]
        assert req["timespan"] == "HOURLY"
        assert req["startTimestamp"] == expected_start
        assert req["endTimestamp"] == expected_end
        d = devices[i]
        assert req["device"] == d
        assert req["readPartition"] == f"{d['customerID']}_{d['deviceID']}"
        assert req["writePartition"] == f"{d['customerID']}_{d['deviceID']}_HOURLY"
