import itertools

import pytest
from tests.conftest import Helpers

from common.models import (
    HTMLMonitorJob,
    JobType,
    ScheduledJob,
    SchedulerChangeEvent,
    SchedulerChangeType,
)


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
            HTMLMonitorJob(
                **Helpers.html_monitor_job_dict_factory(),
                job_type=JobType.HTML_MONITOR_JOB
            ),
        ],
    ),
)
def test_scheduler_change_event_scheduled_job_unpack(
    change_type, job, example_user_email
):
    job_id = 0
    data = SchedulerChangeEvent(
        user_email=example_user_email,
        job_id=job_id,
        change_type=change_type,
        scheduled_job=job,
    ).dict()
    restored = SchedulerChangeEvent(**data)

    assert restored.user_email == example_user_email
    assert restored.job_id == job_id
    assert job.dict() == restored.scheduled_job.dict()


@pytest.mark.parametrize(
    "change_type",
    [
        SchedulerChangeType.CREATE,
        SchedulerChangeType.MODIFY,
        SchedulerChangeType.REMOVE,
    ],
)
def test_scheduler_change_event_scheduled_job_presence_allowed(
    helpers, change_type, example_user_email
):
    job = ScheduledJob(**helpers.scheduled_job_dict_factory(), job_type=JobType.TEST)

    SchedulerChangeEvent(
        user_email=example_user_email,
        job_id=0,
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
    change_type, example_user_email
):
    with pytest.raises(ValueError):
        SchedulerChangeEvent(
            user_email=example_user_email,
            job_id=0,
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
    change_type, example_user_email
):
    SchedulerChangeEvent(
        user_email=example_user_email,
        job_id=0,
        change_type=change_type,
        scheduled_job=None,
    )