import pytest
from pydantic import ValidationError

from common.models import ScheduledJob


@pytest.mark.parametrize(
    "in_data",
    [
        {
            "sleep_time": -1,
        },
        {
            "sleep_time": 0,
        },
    ],
)
def test_scheduled_job_non_positive_sleep_time_error(in_data, helpers):
    try:
        assert ScheduledJob(**helpers.scheduled_job_dict_factory(**in_data))
        assert False
    except ValidationError as e:
        assert "sleepTime must be a positive number" in str(e)
