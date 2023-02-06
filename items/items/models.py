from typing import Union

from pydantic import BaseModel, Extra, HttpUrl, validator


class MonitorJob(BaseModel):
    user_email: str
    job_id: Union[int, None]  # pylint: disable=invalid-name
    make_screenshots: bool = False
    sleep_time: int
    url: HttpUrl

    class Config:
        extra = Extra.forbid

    @validator("sleep_time")
    def sleep_time_must_be_positive(cls, v):
        # pylint: disable=no-self-argument
        # pylint: disable=invalid-name
        if v < 1:
            raise ValueError("sleepTime must be a positive number")
        return v
