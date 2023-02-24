import pytest

from common.models import HTMLMonitorJob, JobType, parse_dict_to_job
from common.models.jobs.utils import map_enum_to_class


def test_parse_dict_to_job_no_job_type(helpers):
    job = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(), job_type=JobType.HTML_MONITOR_JOB
    )

    job_data = job.dict()
    del job_data["job_type"]

    with pytest.raises(ValueError):
        parse_dict_to_job(job_data)


def test_parse_dict_to_job_non_existent_job_type(helpers):
    job = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(), job_type=JobType.HTML_MONITOR_JOB
    )

    job_data = job.dict()

    # Double check that the job_type doesn't exist
    non_existent_job_type = "i-dont-exist"
    with pytest.raises(ValueError):
        JobType(non_existent_job_type)

    job_data["job_type"] = non_existent_job_type

    with pytest.raises(ValueError):
        parse_dict_to_job(job_data)


def test_parse_dict_to_job_html_monitor_job(helpers):
    job = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(), job_type=JobType.HTML_MONITOR_JOB
    )

    job_data = job.dict()

    parsed = parse_dict_to_job(job_data)

    assert parsed.dict() == job.dict()


@pytest.mark.parametrize("entry", list(JobType))
def test_map_enum_to_class_existent(entry):
    map_enum_to_class(entry)


def test_map_enum_to_class_non_existent():
    non_existent = "i-dont-exist"
    # Make sure that value doesn't exist
    with pytest.raises(ValueError):
        JobType(non_existent)

    with pytest.raises(ValueError):
        map_enum_to_class(non_existent)
