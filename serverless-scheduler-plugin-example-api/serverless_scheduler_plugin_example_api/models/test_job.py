from pydantic import validator

from common.models.jobs import ScheduledJob


class TestJob(ScheduledJob):
    __test__ = False

    @validator("job_type")
    def verify_job_type(cls, v):
        expected = "test"
        if v.value != expected:
            raise ValueError(
                f"Incorrect job_type passed: {v.value} instead of {expected}"
            )

        return v
