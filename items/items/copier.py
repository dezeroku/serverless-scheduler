import json
import logging
import os

import boto3
from mypy_boto3_sqs import SQSClient

# from common.models import HTMLMonitorJob

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def copier(event, context):
    # pylint: disable=unused-argument
    records = event["Records"]
    sqs = boto3.client("sqs")
    queue_url = os.environ["OUTPUT_FIFO_SQS_URL"]
    prefix = os.environ["PREFIX"]

    handler(records, sqs, queue_url, prefix)
    # return response
    # return


def handler(records, sqs: SQSClient, queue_url: str, prefix: str):
    for rec in records:
        logger.debug(rec)
        user_email = rec["dynamodb"]["Keys"]["user_email"]["S"].replace("@", "_")
        job_id = rec["dynamodb"]["Keys"]["job_id"]["N"]

        # TODO: parse the record to proper job representation
        # Also add a timestamp to the json, so the deduplication doesn't get
        # too aggresive
        sqs.send_message(
            MessageBody=json.dumps(rec),
            QueueUrl=queue_url,
            MessageGroupId=f"{prefix}-{user_email}-{job_id}"[:127],
        )
