from enum import Enum


# TODO: This is pretty ugly as is and maybe should be made dynamic?
# It looks like a missing design pattern of some kind :D
class JobType(str, Enum):
    Test = "test"
    HTMLMonitorJob = "html_monitor_job"
