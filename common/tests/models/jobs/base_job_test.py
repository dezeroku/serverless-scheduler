import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import integers

from common.models.jobs.base_job import BaseJob


def test_get_unique_job_id_none_job_id(example_user_email):
    job = BaseJob(user_email=example_user_email, job_id=None)

    with pytest.raises(ValueError):
        job.get_unique_job_id()


@given(id_a=integers(), id_b=integers())
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_get_unique_job_id_different_ids(example_user_email, id_a, id_b):
    if id_a != id_b:
        job_a = BaseJob(user_email=example_user_email, job_id=id_a)
        job_b = BaseJob(user_email=example_user_email, job_id=id_b)

        assert job_a.get_unique_job_id() != job_b.get_unique_job_id()
