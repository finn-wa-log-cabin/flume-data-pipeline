import json
from datetime import datetime
from typing import Dict, List

import shared.utils.files as files
import shared.utils.time as time

from InsertSummary import insert_summary

SAMPLES_PATH = "test/InsertSummary/samples/"


def test_insert_summary():
    request_str = files.load_text(SAMPLES_PATH + "request.json")
    data_str = files.load_text(SAMPLES_PATH + "data.json")
    summaries_str = insert_summary.main(request_str, data_str)
    summaries: List[Dict] = json.loads(summaries_str)
    assert len(summaries) == 3

    jan_ts = time.timestamp(datetime(year=2020, month=1, day=1))
    assert summaries[0]["RowKey"] == str(jan_ts)
    assert summaries[0]["startTimestamp"] == jan_ts
    assert summaries[0]["meanData_timestamp"] == jan_ts

    feb_ts = time.timestamp(datetime(year=2020, month=2, day=1))
    assert summaries[1]["RowKey"] == str(feb_ts)
    assert summaries[1]["startTimestamp"] == feb_ts
    assert summaries[1]["meanData_timestamp"] == feb_ts

    mar_ts = time.timestamp(datetime(year=2020, month=3, day=1))
    assert summaries[2]["RowKey"] == str(mar_ts)
    assert summaries[2]["startTimestamp"] == mar_ts
    assert summaries[2]["meanData_timestamp"] == mar_ts

    for summary in summaries:
        assert summary["customerID"] == "TestCustomer1"
        assert summary["deviceID"] == "TestDevice1"
        assert summary["timespan"] == "MONTHLY"
        assert summary["PartitionKey"] == "TestCustomer1_TestDevice1_MONTHLY"
        assert 0 < summary["meanData_humidity"] < 100
        assert 5 < summary["meanData_temperature"] < 30


def test_insert_summary_empty_data():
    request_str = files.load_text(SAMPLES_PATH + "request.json")
    data_str = "[]"
    summaries_str = insert_summary.main(request_str, data_str)
    assert summaries_str == data_str


def test_mean_calculations():
    request_str = files.load_text(SAMPLES_PATH + "request.json")
    data_str = files.load_text(SAMPLES_PATH + "data.json")
    data = json.loads(data_str)
    summaries_str = insert_summary.main(request_str, data_str)
    summaries: List[Dict] = json.loads(summaries_str)

    humidity = "humidity"
    temp = "temperature"
    jan = time.timestamp(datetime(year=2020, month=1, day=1))
    feb = time.timestamp(datetime(year=2020, month=2, day=1))
    mar = time.timestamp(datetime(year=2020, month=3, day=1))
    apr = time.timestamp(datetime(year=2020, month=4, day=1))

    assert summaries[0][f"meanData_{humidity}"] == get_mean(data, humidity, jan, feb)
    assert summaries[0][f"meanData_{temp}"] == get_mean(data, temp, jan, feb)
    assert summaries[1][f"meanData_{humidity}"] == get_mean(data, humidity, feb, mar)
    assert summaries[1][f"meanData_{temp}"] == get_mean(data, temp, feb, mar)
    assert summaries[2][f"meanData_{humidity}"] == get_mean(data, humidity, mar, apr)
    assert summaries[2][f"meanData_{temp}"] == get_mean(data, temp, mar, apr)


def get_mean(data: List[Dict], key: str, start: int, end: int) -> float:
    bin = [
        d[f"sensorData_{key}"] for d in data if start <= d["sensorData_timestamp"] < end
    ]
    return sum(bin) / len(bin)
