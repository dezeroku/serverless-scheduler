from enum import Enum


class SchedulerChangeType(str, Enum):
    # INSERT in dynamodb
    CREATE = "create"
    MODIFY = "modify"
    REMOVE = "remove"
