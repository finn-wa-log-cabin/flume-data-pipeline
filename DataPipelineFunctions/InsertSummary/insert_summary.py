import logging

from azure.functions import QueueMessage


def main(requestMsg: str, dataJson: str) -> None:
    logging.info(f"msg {requestMsg}")
    logging.info(f"data {dataJson}")
