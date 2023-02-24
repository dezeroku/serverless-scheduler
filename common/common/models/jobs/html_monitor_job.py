from pydantic import Field, HttpUrl, validator

from common.models.jobs.job_type import JobType
from common.models.jobs.scheduled_job import ScheduledJob


class HTMLMonitorJob(ScheduledJob):
    job_type: JobType = Field(JobType.HTML_MONITOR_JOB, allow_mutation=False)
    make_screenshots: bool = False
    url: HttpUrl

    class Config:
        validate_assignment = True

    @validator("job_type", pre=True)
    def parse_job_type(cls, _):
        # pylint: disable=no-self-argument
        # JobType always stays the same
        # TODO: a better way to define a default constant?
        return JobType.HTML_MONITOR_JOB
