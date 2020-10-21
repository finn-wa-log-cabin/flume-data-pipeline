import logging

from azure.functions import QueueMessage


def main(requestMsg: QueueMessage, dataJson: str) -> None:
    logging.info(
        "Python queue trigger function processed a queue item: %s",
        requestMsg.get_body().decode("utf-8"),
    )
