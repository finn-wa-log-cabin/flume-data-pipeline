from datetime import datetime, timedelta

import shared.utils.time as time_utils
from dateutil import tz
from dateutil.tz.tz import tzoffset

NZDT = tzoffset("NZDT", timedelta(hours=13).seconds)


def test_timestamp_nzdt():
    dt = datetime(2009, 2, 14, 12, 31, 30, tzinfo=NZDT)
    assert time_utils.timestamp(dt) == 1234567890


def test_timestamp_utc():
    dt = datetime(2009, 2, 13, 23, 31, 31, 11000, tzinfo=tz.UTC)
    assert time_utils.timestamp(dt) == 1234567891


def test_start_of_day_nzdt():
    dt = datetime(2009, 2, 13, 1, 1, 1, 11000, tzinfo=NZDT)
    assert time_utils.start_of_day(dt) == datetime(2009, 2, 13, tzinfo=NZDT)


def test_start_of_day_no_tz():
    dt = datetime(2009, 2, 13, 1, 1, 31, 11000)
    assert time_utils.start_of_day(dt) == datetime(2009, 2, 13)


def test_to_utc_and_back():
    dt_local = datetime(2009, 2, 14, 12, 31, 30, tzinfo=NZDT)
    ts_utc = time_utils.timestamp(dt_local)
    assert ts_utc == 1234567890
    assert (
        time_utils.fromtimestamp(ts_utc).astimezone(tz.gettz("Pacific/Auckland"))
        == dt_local
    )
    assert datetime.fromtimestamp(ts_utc, NZDT) == dt_local
