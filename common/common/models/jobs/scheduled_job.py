from enum import Enum

from pydantic import EmailStr, validator

from common.models.jobs.base_job import BaseJob


class ScheduledJob(BaseJob):
    """
    This class defines the minimum job definition that can be uniquely identified.
    It should be used as a super class for all the jobs that are meant to be run
    periodically (every n seconds)
    """

    # TODO: this is meant to be a way to contact user
    # maybe it's worth abstracting away somehow?
    user_email: EmailStr
    # TODO: this should also be generalized to something like "ScheduleConfig"
    sleep_time: int
    job_type: Enum = None

    @validator("sleep_time")
    def sleep_time_must_be_positive(cls, v):
        # pylint: disable=no-self-argument
        # pylint: disable=invalid-name
        if v < 1:
            raise ValueError("sleepTime must be a positive number")
        return v
