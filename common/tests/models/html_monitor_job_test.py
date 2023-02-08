import pytest
from pydantic import ValidationError

from common.models import HTMLMonitorJob, JobType


def test_monitor_job_immutable_job_type(helpers):
    # with pytest.raises(ValidationError):
    assert HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(), job_type=JobType.Test
    )


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
        assert HTMLMonitorJob(**helpers.html_monitor_job_dict_factory(**in_data))


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
def test_monitor_job_schema_proper_load(in_data, helpers, example_user_email):
    data = HTMLMonitorJob(**helpers.html_monitor_job_dict_factory(**in_data))
    assert data.dict() == {
        "user_email": example_user_email,
        "job_id": 1,
        "make_screenshots": True,
        "sleep_time": 1,
        "url": "http://example.com",
        "job_type": JobType.HTMLMonitorJob,
    }


def test_monitor_job_schema_job_type_default_parse(helpers, example_user_email):
    data = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(), job_type="something-broken"
    )
    assert data.job_type == JobType.HTMLMonitorJob
