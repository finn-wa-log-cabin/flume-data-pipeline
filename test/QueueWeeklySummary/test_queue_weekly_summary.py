import json
from datetime import datetime

from dateutil import tz
from shared.domain.summary_timespan import SummaryTimespan
from shared.utils.files import *
from shared.utils.time import *

from QueueWeeklySummary import queue_weekly_summary as qws

SAMPLES_PATH = "test/QueueWeeklySummary/samples/"


def test_queue_weekly_summary():
    timer_json = load_text(SAMPLES_PATH + "timer.json")
    devices_json = load_text(SAMPLES_PATH + "devices.json")
    nzdt = tz.gettz("Pacific/Auckland")
    expected_start = start_of_day(datetime(2021, 4, 5, tzinfo=nzdt))
    expected_end = start_of(SummaryTimespan.WEEKLY, datetime.now(nzdt))

    requests = json.loads(qws.main(timer_json, devices_json))
    devices = json.loads(devices_json)
    for i in range(len(requests)):
        req = requests[i]
        assert req["timespan"] == "WEEKLY"
        assert fromtimestamp(req["startTimestamp"]) == expected_start
        assert fromtimestamp(req["endTimestamp"]) == expected_end
        d = devices[i]
        assert req["device"] == d
        assert req["readPartition"] == f"{d['customerID']}_{d['deviceID']}"
        assert req["writePartition"] == f"{d['customerID']}_{d['deviceID']}_WEEKLY"
