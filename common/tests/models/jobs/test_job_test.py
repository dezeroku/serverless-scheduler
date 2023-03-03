from common.models.plugins import JobType, TestJob


def test_test_job_creation(helpers):
    TestJob(**helpers.test_job_dict_factory())


def test_test_job_type(helpers):
    TestJob(**helpers.test_job_dict_factory()).job_type == JobType.TEST
