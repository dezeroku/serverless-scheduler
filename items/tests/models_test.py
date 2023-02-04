import pytest
from pydantic import ValidationError

from items.models import MonitorJob


@pytest.mark.parametrize(
    "in_data",
    [
        {
            "url": "broken-url",
        },
        {
            "url": "http://no-tld",
        },
    ],
)
def test_monitor_job_schema_load_url_validates(in_data, helpers):
    with pytest.raises(ValidationError):
        assert MonitorJob(**helpers.MonitorJobJSONFactory(**in_data))


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
def test_monitor_job_schema_load_nonpositive_sleep_time_error(in_data, helpers):
    try:
        assert MonitorJob(**helpers.MonitorJobJSONFactory(**in_data))
        assert False
    except ValidationError as e:
        assert "sleepTime must be a positive number" in str(e)


@pytest.mark.parametrize(
    "in_data",
    [
        {
            "job_id": 1,
            "make_screenshots": True,
            "sleep_time": 1,
            "url": "http://example.com",
        }
    ],
)
def test_monitor_job_schema_proper_load(in_data, helpers, db_user):
    data = MonitorJob(**helpers.MonitorJobJSONFactory(**in_data))
    assert data.dict() == {
        "user_id": db_user,
        "job_id": 1,
        "make_screenshots": True,
        "sleep_time": 1,
        "url": "http://example.com",
    }
