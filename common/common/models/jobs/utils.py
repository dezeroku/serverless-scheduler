from enum import Enum

from common.models.jobs.html_monitor_job import HTMLMonitorJob
from common.models.jobs.job_type import JobType
from common.models.jobs.scheduled_job import ScheduledJob


def map_enum_to_class(entry: Enum):
    # TODO: similar to JobType, this really looks like it needs some design pattern
    if entry == JobType.TEST:
        return ScheduledJob

    if entry == JobType.HTML_MONITOR_JOB:
        return HTMLMonitorJob

    raise ValueError(f"No matching JobType found for {str(entry)}")


def parse_dict_to_job(data: dict):
    if not (job_type := data.get("job_type")):
        raise ValueError("No job_type provided")

    try:
        job_type_enum = JobType(job_type)
    except ValueError as exc:
        raise ValueError("Incorrect job_type provided") from exc

    job_class = map_enum_to_class(job_type_enum)
    return job_class(**data)
