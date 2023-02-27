import json
import logging
import os

import boto3
from mypy_boto3_scheduler import EventBridgeSchedulerClient

from common.models import SchedulerChangeEvent, SchedulerChangeType
from schedulers.scheduler_manager import SchedulerManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def schedule_controller(event, context):
    # pylint: disable=unused-argument
    sns_topic_arn = os.environ["DISTRIBUTION_SNS_TOPIC_ARN"]
    scheduler = boto3.client("scheduler")
    scheduler_group = os.environ["SCHEDULERS_GROUP"]
    scheduler_role_arn = os.environ["SCHEDULERS_ROLE_ARN"]

    failed_ids = handler(
        event["Records"], sns_topic_arn, scheduler, scheduler_group, scheduler_role_arn
    )
    return {"batchItemFailures": [{"itemIdentifier": fid} for fid in failed_ids]}


def handler(
    records: list,
    sns_topic_arn: str,
    scheduler: EventBridgeSchedulerClient,
    scheduler_group: str,
    scheduler_role_arn: str,
):
    message_ids = list(map(lambda x: x["messageId"], records))
    try:
        for rec in records:
            change_event = SchedulerChangeEvent(**json.loads(rec["body"]))

            if change_event.change_type == SchedulerChangeType.REMOVE:
                job = None
            else:
                job = change_event.scheduled_job

            manager = SchedulerManager(
                scheduler, scheduler_group, change_event.scheduler_id, job
            )

            if change_event.change_type == SchedulerChangeType.CREATE:
                manager.create(sns_topic_arn, scheduler_role_arn)
            elif change_event.change_type == SchedulerChangeType.MODIFY:
                manager.update(sns_topic_arn, scheduler_role_arn)
            elif change_event.change_type == SchedulerChangeType.REMOVE:
                manager.delete()
            else:
                raise ValueError(
                    f"Not supported change_type: {change_event.change_type}"
                )

            message_ids.pop(0)
    except Exception as exc:
        # pylint: disable=broad-exception-caught
        # This is being a little lazy, but it really doesn't matter what goes wrong here
        logger.error(
            "Encountered an exception processing %s : %s", rec["messageId"], exc
        )
        raise exc

    # Returns a list of messageIDs that couldn't be processed successfully
    # It stops processing on the first failure and returns the failed + all
    # unprocessed event IDs (because of the input queue being a FIFO)
    return message_ids
