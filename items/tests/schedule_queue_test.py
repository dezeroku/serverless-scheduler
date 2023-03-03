import json

import pytest
from mypy_boto3_sqs import SQSClient

from common.models.events import SchedulerChangeEvent, SchedulerChangeType

# pylint: disable=no-name-in-module
from common.models.plugins import HTMLMonitorJob, parse_dict_to_job
from items.schedule_queue import dynamodb_to_typed_dict, handler


@pytest.mark.parametrize(
    "inp,output",
    [
        ({"field1": {"S": "string"}}, {"field1": "string"}),
        (
            {"field1": {"S": "string"}, "field2": {"N": "123"}},
            {"field1": "string", "field2": 123},
        ),
        (
            {
                "field1": {"S": "string"},
                "field2": {"N": "123"},
                "field3": {"BOOL": "true"},
            },
            {"field1": "string", "field2": 123, "field3": True},
        ),
        (
            {
                "field1": {"S": "string"},
                "field2": {"N": "123"},
                "field3": {"BOOL": "false"},
            },
            {"field1": "string", "field2": 123, "field3": False},
        ),
    ],
)
def test_dynamodb_to_typed_dict_correct(inp, output):
    assert dynamodb_to_typed_dict(inp) == output


def test_dynamodb_to_typed_dict_nonexistent_type():
    with pytest.raises(ValueError):
        dynamodb_to_typed_dict({"field1": {"NON-EXISTENT-TYPE": 0}})


def minimal_dynamodb_stream_record_html_monitor_job(
    event_name: str, html_monitor_job: HTMLMonitorJob, timestamp=0.0
):
    allowed_event_names = ("MODIFY", "INSERT", "REMOVE")
    if event_name not in allowed_event_names:
        raise ValueError(f"Incorrect event_name, not one of {allowed_event_names}")

    return {
        "eventName": event_name,
        "dynamodb": {
            "ApproximateCreationDateTime": timestamp,
            "Keys": {
                "user_id": {"S": html_monitor_job.user_id},
                "job_id": {"N": str(html_monitor_job.job_id)},
            },
            "NewImage": {
                "job_type": {"S": str(html_monitor_job.job_type.value)},
                "user_id": {"S": html_monitor_job.user_id},
                "user_email": {"S": html_monitor_job.user_email},
                "job_id": {"N": str(html_monitor_job.job_id)},
                "sleep_time": {"N": str(html_monitor_job.sleep_time)},
                "url": {"S": str(html_monitor_job.url)},
                "make_screenshots": {"BOOL": html_monitor_job.make_screenshots},
            },
        },
    }


def test_handler_html_monitor_job_different_types(
    helpers,
    mock_sqs: SQSClient,
    example_queue_name: str,
):
    change_type_strs = ["INSERT", "MODIFY", "REMOVE"]
    change_types = [
        SchedulerChangeType.CREATE,
        SchedulerChangeType.MODIFY,
        SchedulerChangeType.REMOVE,
    ]
    jobs = [
        parse_dict_to_job(helpers.html_monitor_job_dict_factory(job_id=0)),
        parse_dict_to_job(helpers.html_monitor_job_dict_factory(job_id=0)),
        parse_dict_to_job(helpers.html_monitor_job_dict_factory(job_id=0)),
    ]

    expected_change_events = [
        SchedulerChangeEvent(
            scheduler_id=job.get_unique_job_id(),
            change_type=change_type,
            scheduled_job=job,
            timestamp=0.0,
        )
        for job, change_type in list(zip(jobs, change_types))[:-1]
    ]

    expected_change_events.append(
        SchedulerChangeEvent(
            scheduler_id=jobs[-1].get_unique_job_id(),
            change_type=change_types[-1],
            scheduled_job=None,
            timestamp=0.0,
        )
    )

    handler_generic_html_monitor_job(
        mock_sqs, example_queue_name, jobs, change_type_strs, expected_change_events
    )


@pytest.mark.parametrize(
    "change_type,change_type_str,number_of_jobs",
    [
        (SchedulerChangeType.MODIFY, "MODIFY", 5),
        (SchedulerChangeType.CREATE, "INSERT", 5),
    ],
)
def test_handler_html_monitor_job(
    helpers,
    mock_sqs: SQSClient,
    example_queue_name: str,
    change_type: SchedulerChangeType,
    change_type_str: str,
    number_of_jobs: int,
):
    change_type_strs = [change_type_str for _ in range(number_of_jobs)]
    change_types = [change_type for _ in range(number_of_jobs)]
    jobs = [
        parse_dict_to_job(helpers.html_monitor_job_dict_factory(job_id=x))
        for x in range(number_of_jobs)
    ]

    expected_change_events = [
        SchedulerChangeEvent(
            scheduler_id=job.get_unique_job_id(),
            change_type=change_type,
            scheduled_job=job,
            timestamp=0.0,
        )
        for job, change_type in zip(jobs, change_types)
    ]
    handler_generic_html_monitor_job(
        mock_sqs,
        example_queue_name,
        jobs,
        change_type_strs,
        expected_change_events,
        number_of_jobs + 5,
    )


@pytest.mark.parametrize("number_of_jobs", range(1, 5))
def test_handler_html_monitor_job_remove_multi_messages(
    helpers, mock_sqs: SQSClient, example_queue_name: str, number_of_jobs: int
):
    change_type_strs = ["REMOVE" for _ in range(number_of_jobs)]
    change_types = [SchedulerChangeType.REMOVE for _ in range(number_of_jobs)]
    jobs = [
        parse_dict_to_job(helpers.html_monitor_job_dict_factory(job_id=x))
        for x in range(number_of_jobs)
    ]

    expected_change_events = [
        SchedulerChangeEvent(
            scheduler_id=job.get_unique_job_id(),
            change_type=change_type,
            scheduled_job=None,
            timestamp=0.0,
        )
        for job, change_type in zip(jobs, change_types)
    ]

    handler_generic_html_monitor_job(
        mock_sqs,
        example_queue_name,
        jobs,
        change_type_strs,
        expected_change_events,
        number_of_jobs + 5,
    )


def handler_generic_html_monitor_job(
    sqs: SQSClient,
    queue_name: str,
    jobs: list[HTMLMonitorJob],
    change_type_strs: list[str],
    expected_change_events: list[SchedulerChangeEvent],
    max_number_of_messages: int = 5,
):
    queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]

    assert len(jobs) == len(change_type_strs) == len(expected_change_events)

    records = [
        minimal_dynamodb_stream_record_html_monitor_job(change_type_str, x)
        for change_type_str, x in zip(change_type_strs, jobs)
    ]

    handler(records, sqs, queue_url)

    messages = sqs.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=max_number_of_messages
    )["Messages"]
    assert len(messages) == len(jobs)

    message_bodies = map(lambda x: x["Body"], messages)

    for expected_change_event, message_body in zip(
        expected_change_events, message_bodies
    ):
        received_change_event_dict = json.loads(message_body)
        received_change_event = SchedulerChangeEvent(**received_change_event_dict)

        assert received_change_event.dict() == expected_change_event.dict()
