import pytest
from pydantic import ValidationError

from common.models import HTMLMonitorJob, JobType


def test_monitor_job_immutable_job_type(helpers):
    # with pytest.raises(ValidationError):
    test = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(), job_type=JobType.TEST
    )

    assert test.job_type == JobType.HTML_MONITOR_JOB


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
def test_monitor_job_schema_proper_load(
    in_data, helpers, example_user_email, example_user_id
):
    data = HTMLMonitorJob(**helpers.html_monitor_job_dict_factory(**in_data))
    assert data.dict() == {
        "user_id": example_user_id,
        "user_email": example_user_email,
        "job_id": 1,
        "make_screenshots": True,
        "sleep_time": 1,
        "url": "http://example.com",
        "job_type": JobType.HTML_MONITOR_JOB,
    }


def test_monitor_job_schema_job_type_default_parse(helpers):
    data = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(), job_type="something-broken"
    )
    assert data.job_type == JobType.HTML_MONITOR_JOB
