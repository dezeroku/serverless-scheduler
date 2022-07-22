from dataclasses import dataclass
from typing import List


@dataclass
class MonitorJob:
    id: int
    make_screenshots: bool
    sleep_time: int
    url: str


@dataclass
class UserData:
    id: str
    monitors: List[MonitorJob]
