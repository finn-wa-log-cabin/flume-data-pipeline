from main.common.utils.files import *
from main.InsertSummary.insert_summary import *

SAMPLES_PATH = "test/InsertSummary/samples/"


def test_insert_summary():
    request_str = load_text(SAMPLES_PATH + "request.json")
    data_str = load_text(SAMPLES_PATH + "data.json")
    main(request_str, data_str)
    assert True
