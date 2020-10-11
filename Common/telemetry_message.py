import json


class TelemetryMessage:
    deviceId: str
    messageId: int
    depth: int

    def __init__(self, json_raw: str):
        """ Deserialises a TelemetryMessage from a JSON string. """
        json_dict = json.loads(json_raw)
        self.deviceId = json_dict["deviceId"]
        self.messageId = json_dict["messageId"]
        self.depth = json_dict["depth"]

    def get_partition_raw(self):
        """ Returns the partition name for the specified device. """
        return f"{self.deviceId}_raw"
