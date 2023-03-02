import itertools
from datetime import datetime

import pytest
from tests.conftest import Helpers

# Pylint doesn't respect the plugin thingy :/
# pylint: disable=no-name-in-module
from common.models import JobType, ScheduledJob, TestJob
from common.models.events import SchedulerChangeEvent, SchedulerChangeType


@pytest.fixture(name="example_scheduler_id")
def example_scheduler_id_fixture():
    return "user-email-job-id"


@pytest.mark.parametrize(
    "change_type,job",
    itertools.product(
        [
            SchedulerChangeType.CREATE,
            SchedulerChangeType.MODIFY,
            SchedulerChangeType.REMOVE,
        ],
        [
            ScheduledJob(**Helpers.scheduled_job_dict_factory(), job_type=JobType.TEST),
            TestJob(**Helpers.test_job_dict_factory(), job_type=JobType.TEST),
        ],
    ),
)
def test_scheduler_change_event_scheduled_job_unpack(change_type, job: ScheduledJob):
    data = SchedulerChangeEvent(
        scheduler_id=job.get_unique_job_id(),
        change_type=change_type,
        scheduled_job=job,
    ).dict()
    restored = SchedulerChangeEvent(**data)

    assert restored.scheduler_id == job.get_unique_job_id()
    assert job.dict() == restored.scheduled_job.dict()


@pytest.mark.parametrize(
    "change_type",
    [
        SchedulerChangeType.CREATE,
        SchedulerChangeType.MODIFY,
        SchedulerChangeType.REMOVE,
    ],
)
def test_scheduler_change_event_scheduled_job_presence_allowed(helpers, change_type):
    job = ScheduledJob(**helpers.scheduled_job_dict_factory(), job_type=JobType.TEST)

    SchedulerChangeEvent(
        scheduler_id=job.get_unique_job_id(),
        change_type=change_type,
        scheduled_job=job,
    )


@pytest.mark.parametrize(
    "change_type",
    [
        SchedulerChangeType.CREATE,
        SchedulerChangeType.MODIFY,
    ],
)
def test_scheduler_change_event_scheduled_job_presence_required(
    change_type, example_scheduler_id
):
    with pytest.raises(ValueError):
        SchedulerChangeEvent(
            scheduled_id=example_scheduler_id,
            change_type=change_type,
            scheduled_job=None,
        )


@pytest.mark.parametrize(
    "change_type",
    [
        SchedulerChangeType.REMOVE,
    ],
)
def test_scheduler_change_event_scheduled_job_presence_allowed_none(
    change_type, example_scheduler_id
):
    SchedulerChangeEvent(
        scheduler_id=example_scheduler_id,
        change_type=change_type,
        scheduled_job=None,
    )


def test_scheduler_change_event_none_timestamp(example_scheduler_id):
    SchedulerChangeEvent(
        scheduler_id=example_scheduler_id,
        change_type=SchedulerChangeType.REMOVE,
        scheduled_job=None,
        timestamp=None,
    )


@pytest.mark.parametrize(
    "timestamp_type",
    [
        int,
        float,
    ],
)
def test_scheduler_change_event_timestamp_from_type(
    example_scheduler_id, timestamp_type
):
    timestamp = 0
    event = SchedulerChangeEvent(
        scheduler_id=example_scheduler_id,
        change_type=SchedulerChangeType.REMOVE,
        scheduled_job=None,
        timestamp=timestamp_type(timestamp),
    )

    assert event.timestamp.timestamp() == timestamp


def test_scheduler_change_event_timestamp_from_datetime(example_scheduler_id):
    timestamp = datetime.fromtimestamp(0)
    event = SchedulerChangeEvent(
        scheduler_id=example_scheduler_id,
        change_type=SchedulerChangeType.REMOVE,
        scheduled_job=None,
        timestamp=timestamp,
    )

    assert event.timestamp == timestamp


def test_scheduler_change_event_timestamp_from_string(example_scheduler_id):
    timestamp_string = "1970-01-01T00:00:00+00:00"
    timestamp = datetime.fromisoformat(timestamp_string)
    event = SchedulerChangeEvent(
        scheduler_id=example_scheduler_id,
        change_type=SchedulerChangeType.REMOVE,
        scheduled_job=None,
        timestamp=timestamp_string,
    )

    assert event.timestamp == timestamp
