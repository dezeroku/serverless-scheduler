import logging
import os

import boto3
from mypy_boto3_sqs import SQSClient

from common.models import (
    BaseJob,
    SchedulerChangeEvent,
    SchedulerChangeType,
    parse_dict_to_job,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def dynamodb_to_typed_dict(entry: dict):
    key_type_mapping = {
        "S": str,
        "N": float,
        "BOOL": lambda x: x in (True, "true"),
    }

    for key, val in entry.items():
        match_found = False
        for map_key, convert_func in key_type_mapping.items():
            if map_key in val:
                entry[key] = convert_func(val[map_key])
                match_found = True
                break

        if not match_found:
            raise ValueError(f"Mapping type not found for {val}")

    return entry


def add(event, context):
    # pylint: disable=unused-argument
    records = event["Records"]
    sqs = boto3.client("sqs")
    queue_url = os.environ["OUTPUT_FIFO_SQS_URL"]

    handler(records, sqs, queue_url)


def handler(records, sqs: SQSClient, queue_url: str):
    scheduler_change_type_map = {
        "INSERT": SchedulerChangeType.CREATE,
        "MODIFY": SchedulerChangeType.MODIFY,
        "REMOVE": SchedulerChangeType.REMOVE,
    }

    for rec in records:
        logger.debug(rec)
        rec["dynamodb"]["Keys"] = dynamodb_to_typed_dict(rec["dynamodb"]["Keys"])

        user_email = rec["dynamodb"]["Keys"]["user_email"]
        job_id = rec["dynamodb"]["Keys"]["job_id"]
        timestamp = rec["dynamodb"]["ApproximateCreationDateTime"]

        change_type = scheduler_change_type_map[rec["eventName"]]
        if change_type == SchedulerChangeType.REMOVE:
            scheduled_job = None
            # Get job ID using base class
            base_job = BaseJob(user_email=user_email, job_id=job_id)
            scheduler_id = base_job.get_unique_job_id()
        else:
            new_image = dynamodb_to_typed_dict(rec["dynamodb"]["NewImage"])
            scheduled_job = parse_dict_to_job(new_image)
            scheduler_id = scheduled_job.get_unique_job_id()

        change_event = SchedulerChangeEvent(
            scheduler_id=scheduler_id,
            change_type=change_type,
            scheduled_job=scheduled_job,
            timestamp=timestamp,
        )

        sqs.send_message(
            MessageBody=change_event.json(),
            QueueUrl=queue_url,
            MessageGroupId=scheduler_id,
        )
