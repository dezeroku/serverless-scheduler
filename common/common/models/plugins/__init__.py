import os
import sys
from enum import Enum

from common.models.jobs import parse_dict_to_job_factory
from common.models.plugins.plugins import discover_plugins

_PLUGINS_SEARCH_PREFIX = os.getenv(
    "_COMMON_PACKAGE_PLUGINS_SEARCH_PREFIX", "serverless_scheduler_"
)

(
    _PLUGINS_ENUM_MAPPING,
    _PLUGINS_CLASS_MAPPING,
    PLUGINS_ALL_CLASSES_LIST,
) = discover_plugins(_PLUGINS_SEARCH_PREFIX)


JobType = Enum("JobType", _PLUGINS_ENUM_MAPPING, type=str)

# Convert the class mapping, so map_enum_to_class recognizes enum values, not strings
_PLUGINS_CLASS_MAPPING = {JobType(k): v for k, v in _PLUGINS_CLASS_MAPPING.items()}

# Even though we loaded the module, we also need to expose the classes
# This looks sketchy, but should be fine I guess
for cls in _PLUGINS_CLASS_MAPPING.values():
    setattr(sys.modules[__name__], cls.__name__, cls)


def map_enum_to_class(entry: JobType):
    try:
        return _PLUGINS_CLASS_MAPPING[entry]
    except KeyError as exc:
        raise ValueError(f"No matching JobType found for {str(entry)}") from exc


parse_dict_to_job = parse_dict_to_job_factory(JobType, map_enum_to_class)
