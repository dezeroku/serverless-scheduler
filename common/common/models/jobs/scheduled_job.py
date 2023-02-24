from pydantic import validator

from common.models.jobs.base_job import BaseJob
from common.models.jobs.job_type import JobType


class ScheduledJob(BaseJob):
    sleep_time: int
    job_type: JobType = None

    @validator("sleep_time")
    def sleep_time_must_be_positive(cls, v):
        # pylint: disable=no-self-argument
        # pylint: disable=invalid-name
        if v < 1:
            raise ValueError("sleepTime must be a positive number")
        return v
