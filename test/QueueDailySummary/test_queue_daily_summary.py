import json
from datetime import datetime, timedelta

from dateutil import tz, utils
from dateutil.tz.tz import tzoffset
from shared.utils.files import *
from shared.utils.time import as_utc, start_of_day, timestamp

from QueueDailySummary import queue_daily_summary as qds

SAMPLES_PATH = "test/QueueDailySummary/samples/"


def test_queue_daily_summary():
    timer_json = load_text(SAMPLES_PATH + "timer.json")
    devices_json = load_text(SAMPLES_PATH + "devices.json")
    nzdt = tzoffset("NZDT", timedelta(hours=13))
    expected_start = timestamp(
        start_of_day(as_utc(datetime(2020, 10, 19, tzinfo=nzdt)))
    )
    expected_end = timestamp(utils.today(tzinfo=tz.UTC))

    requests = json.loads(qds.main(timer_json, devices_json))
    devices = json.loads(devices_json)
    for i in range(len(requests)):
        req = requests[i]
        assert req["timespan"] == "DAILY"
        assert req["startTimestamp"] == expected_start
        assert req["endTimestamp"] == expected_end
        d = devices[i]
        assert req["device"] == d
        assert req["readPartition"] == f"{d['customerID']}_{d['deviceID']}"
        assert req["writePartition"] == f"{d['customerID']}_{d['deviceID']}_DAILY"
