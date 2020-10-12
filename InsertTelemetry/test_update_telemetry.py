import json
from datetime import datetime

from pytest_mock.plugin import MockerFixture

from InsertTelemetry.insert_telemetry import main


def get_mock_event(mocker: MockerFixture) -> any:
    with open("InsertTelemetry/example_telemetry.json", "r") as file:
        example_msg = file.read()
    example_telemetry = mocker.Mock()
    example_telemetry.get_json.return_value = example_msg
    return example_telemetry


def test_update_telemetry(mocker: MockerFixture):
    timestamp = float(1602495228411)
    event = get_mock_event(mocker)
    event.event_time.return_value = datetime.fromtimestamp(timestamp / 1000)

    row = main(event)
    row_dict = json.loads(row)
    assert row_dict["PartitionKey"] == "FeatherHuzzah1_Raw"
    assert row_dict["RowKey"] == str(int(timestamp))
    assert row_dict["messageID"] == 12
    assert row_dict["deviceID"] == "FeatherHuzzah1"
    assert row_dict["depth"] == 100


def test_update_telemetry_no_event_time(mocker: MockerFixture):
    event = get_mock_event(mocker)
    event.event_time.return_value = None

    row = main(event)
    row_dict = json.loads(row)
    assert row_dict["PartitionKey"] == "FeatherHuzzah1_Raw"
    assert isinstance(row_dict["RowKey"], str)
    assert len(row_dict["RowKey"]) == 13
    assert row_dict["messageID"] == 12
    assert row_dict["deviceID"] == "FeatherHuzzah1"
    assert row_dict["depth"] == 100
