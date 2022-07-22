from typing import List
from dataclasses import dataclass


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
