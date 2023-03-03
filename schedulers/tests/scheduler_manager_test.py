from types import SimpleNamespace

import pytest

from common.models.jobs import ScheduledJob
from schedulers.scheduler_manager import SchedulerManager


@pytest.mark.parametrize(
    "sleep_time,result",
    [
        (1, "rate(1minute)"),
        (61, "rate(2minutes)"),
        (120, "rate(2minutes)"),
        (121, "rate(3minutes)"),
        (599, "rate(10minutes)"),
        (600, "rate(10minutes)"),
    ],
)
def test_scheduler_manager_get_schedule_expression(
    helpers, sleep_time: int, result: str
):
    job = ScheduledJob(**helpers.scheduled_job_dict_factory(sleep_time=sleep_time))

    assert SchedulerManager.get_schedule_expression(job) == result


def test_scheduler_manager_get_schedule_expression_requires_positive_sleep_time():
    # This is a very naive way to test it, but works for our needs
    # It's also handled on the model's level, this is just an additional precaution
    payload = SimpleNamespace(sleep_time=0)
    with pytest.raises(ValueError):
        SchedulerManager.get_schedule_expression(payload)
