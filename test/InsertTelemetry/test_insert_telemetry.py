import json
from base64 import b64encode

import main.InsertTelemetry.insert_telemetry as it
from main.common.utils.files import *
from pytest_mock.plugin import MockerFixture

SAMPLES_PATH = "test/InsertTelemetry/samples/"


def get_mock_event(mocker: MockerFixture):
    telemetry = load_json(SAMPLES_PATH + "telemetry.json")
    body = load_text(SAMPLES_PATH + "body.json")
    telemetry["body"] = b64encode(body.encode()).decode()
    event_msg = mocker.Mock()
    event_msg.get_json.return_value = telemetry
    return event_msg


def test_insert_telemetry(mocker: MockerFixture):
    event = get_mock_event(mocker)
    row = it.main(event)
    row_dict = json.loads(row)
    assert row_dict["PartitionKey"] == "TestCustomer_TestDevice1"
    assert row_dict["RowKey"] == "1602495228411"
    assert row_dict["deviceID"] == "TestDevice1"
    assert row_dict["customerID"] == "TestCustomer"
    assert row_dict["depth"] == 300
    assert row_dict["eventTimestamp"] == 1602495228411
    assert row_dict["messageCount"] == 24
