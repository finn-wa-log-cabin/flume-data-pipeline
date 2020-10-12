import logging

from azure.functions import QueueMessage
from azure.cosmosdb.table import Entity


def main(requestMsg: QueueMessage, data: str) -> None:
    logging.info("Python queue trigger function processed a queue item: %s", requestMsg.get_body().decode("utf-8"))
