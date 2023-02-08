from typing import Union

from pydantic import BaseModel, EmailStr, Extra, validator

from common.models.job_type import JobType


class ScheduledJob(BaseModel):
    user_email: EmailStr
    job_id: Union[int, None]  # pylint: disable=invalid-name
    sleep_time: int
    job_type: JobType = None

    class Config:
        extra = Extra.forbid

    @validator("sleep_time")
    def sleep_time_must_be_positive(cls, v):
        # pylint: disable=no-self-argument
        # pylint: disable=invalid-name
        if v < 1:
            raise ValueError("sleepTime must be a positive number")
        return v
