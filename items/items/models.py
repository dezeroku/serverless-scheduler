from dataclasses import dataclass
from typing import List


@dataclass
class MonitorJob:
    id: int  # pylint: disable=invalid-name
    make_screenshots: bool
    sleep_time: int
    url: str


@dataclass
class UserData:
    id: str  # pylint: disable=invalid-name
    monitors: List[MonitorJob]
