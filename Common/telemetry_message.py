import json


class TelemetryMessage:
    device_id: str
    message_id: int
    depth: int

    def __init__(self, json_raw: str):
        """
        Deserialises a TelemetryMessage from a JSON string.
        """
        json_dict = json.loads(json_raw)
        self.device_id = json_dict["deviceId"]
        self.message_id = json_dict["messageId"]
        self.depth = json_dict["depth"]

    def get_partition_raw(self):
        """
        Returns the partition name for the specified device.
        """
        return f"{self.device_id}_Raw"
