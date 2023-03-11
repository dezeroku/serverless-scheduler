from datetime import datetime
from typing import Union

from pydantic import BaseModel, Extra, validator

from common.models.events.scheduler_change_type import SchedulerChangeType
from common.models.jobs.scheduled_job import ScheduledJob
from common.models.plugins import parse_dict_to_job


class SchedulerChangeEvent(BaseModel):
    """
    Defines event that is sent to "Output" SQS at the end of the "items" flow.
    It's also the input for "schedulers" flow.
    """

    scheduler_id: str
    change_type: SchedulerChangeType
    # Set to none in case of REMOVE event
    # This is duplicated a bit, as the job_id and user_email are also provided in the class itself
    # The reasoning behind it is that if you get a REMOVE event, you don't get a scheduled_job
    # object at all and you still need to uniquely identify the EventBridge Scheduler to modify.
    scheduled_job: Union[ScheduledJob, None]

    timestamp: Union[datetime, None] = None

    class Config:
        extra = Extra.forbid

    @validator("scheduled_job", pre=True)
    def parse_dict_to_job(cls, v):
        # pylint: disable=no-self-argument,invalid-name
        if isinstance(v, dict):
            return parse_dict_to_job(v)

        return v

    @validator("scheduled_job")
    def parse_job_type(cls, v, values: dict):
        # pylint: disable=no-self-argument,invalid-name
        if change_type := values.get("change_type"):
            if change_type in (SchedulerChangeType.CREATE, SchedulerChangeType.MODIFY):
                if v is None:
                    raise ValueError(
                        "scheduled_job needs to be provided if change_type is CREATE or MODIFY"
                    )

        return v
