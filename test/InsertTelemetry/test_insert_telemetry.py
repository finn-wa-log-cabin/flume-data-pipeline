import json

import main.InsertTelemetry.insert_telemetry as it
from main.common.utils.files import *
from pytest_mock.plugin import MockerFixture

SAMPLES_PATH = "test/InsertTelemetry/samples/"


def get_mock_event(mocker: MockerFixture) -> any:
    example_msg = load_json(SAMPLES_PATH + "telemetry.json")
    example_telemetry = mocker.Mock()
    example_telemetry.get_json.return_value = example_msg
    return example_telemetry


def test_insert_telemetry(mocker: MockerFixture):
    event = get_mock_event(mocker)
    row = it.main(event)
    row_dict = json.loads(row)
    assert row_dict["PartitionKey"] == "TestCustomer_TestDevice1_Raw"
    assert row_dict["RowKey"] == "1602495228411"
    assert row_dict["deviceID"] == "TestDevice1"
    assert row_dict["customerID"] == "TestCustomer"
    assert row_dict["depth"] == 300
    assert row_dict["period"] == {"name": "Raw", "days": 0}
