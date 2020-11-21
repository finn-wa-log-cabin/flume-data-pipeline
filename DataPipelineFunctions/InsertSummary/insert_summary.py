import json
import logging
from typing import Dict, List


def main(requestMsg: str, dataJson: str) -> str:
    request: Dict = json.loads(requestMsg)
    data: List[Dict] = json.loads(dataJson)
    depth_readings = [d["depth"] for d in data if isinstance(d, int)]
    if len(depth_readings) == 0:
        logging.warn(f"No valid readings for summary request {requestMsg}")
    elif len(depth_readings) != len(data):
        logging.warn(f"Discarded invalid readings from {data} to produce {depth_readings}")
    else:
        summary = {
            "deviceID": request["device"]["deviceID"],
            "customerID": request["device"]["customerID"],
            "periodName": request["periodName"],
            "startTime": request["startTime"],
            "endTime": request["endTime"],
            "averageDepth": sum(depth_readings) / len(depth_readings),
            "numReadings": len(depth_readings),
        }
        return json.dumps(summary)
