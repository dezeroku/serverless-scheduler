# pylint: disable=no-name-in-module
from common.models.plugins import JobType, parse_dict_to_job


def test_test_job_creation(helpers):
    parse_dict_to_job(helpers.test_job_dict_factory())


def test_test_job_type(helpers):
    assert parse_dict_to_job(helpers.test_job_dict_factory()).job_type == JobType.TEST
