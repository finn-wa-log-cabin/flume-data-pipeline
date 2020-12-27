import json
from main.common.utils.files import *
from datetime import datetime, timedelta

import main.QueueDailySummary.queue_daily_summary as qds
from dateutil import tz, utils
from dateutil.tz.tz import tzoffset
from main.common.utils.time import as_utc, start_of_day, timestamp

SAMPLES_PATH = "test/QueueDailySummary/samples/"


def test_queue_daily_summary():
    timer_json = load_text(SAMPLES_PATH + "timer.json")
    devices_json = load_text(SAMPLES_PATH + "devices.json")
    nzdt = tzoffset("NZDT", timedelta(hours=13))
    expected_period = {"name": "Daily", "days": 1}
    expected_start = timestamp(start_of_day(as_utc(datetime(2020, 10, 19, tzinfo=nzdt))))
    expected_end = timestamp(utils.today(tzinfo=tz.UTC))

    requests = json.loads(qds.main(timer_json, devices_json))
    devices = json.loads(devices_json)
    for i in range(len(requests)):
        req = requests[i]
        assert req["period"]["name"] == expected_period["name"]
        assert req["period"]["days"] == expected_period["days"]
        assert req["startTimestamp"] == expected_start
        assert req["endTimestamp"] == expected_end
        d = devices[i]
        assert req["device"] == d
        assert req["readPartition"] == f"{d['customerID']}_{d['deviceID']}_Raw"
        assert req["writePartition"] == f"{d['customerID']}_{d['deviceID']}_Daily"
