from pydantic import validator

from common.models.jobs.base_job import BaseJob
from common.models.jobs.job_type import JobType


class ScheduledJob(BaseJob):
    """
    This class defines the minimum job definition that can be uniquely identified.
    It should be used as a super class for all the jobs that are meant to be run
    periodically (every n seconds)
    """

    sleep_time: int
    job_type: JobType = None

    @validator("sleep_time")
    def sleep_time_must_be_positive(cls, v):
        # pylint: disable=no-self-argument
        # pylint: disable=invalid-name
        if v < 1:
            raise ValueError("sleepTime must be a positive number")
        return v
