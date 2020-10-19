import json
from datetime import datetime

from pytest_mock.plugin import MockerFixture

from DataPipelineFunctions.QueueDailySummary.queue_daily_summary import main

TEST_DIR = "DataPipelineTests/QueueDailySummary/"


def get_timer_json() -> str:
    with open(TEST_DIR + "timer.json", "r") as timer_file:
        return timer_file.read()


# def get_devices_json


# def test_update_telemetry(mocker: MockerFixture):
