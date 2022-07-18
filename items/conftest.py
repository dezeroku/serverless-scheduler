import pytest

from schemas import MonitorJobSchema, UserDataSchema
from models import MonitorJob, UserData

@pytest.fixture
def example_user_data(example_monitor_job):
    temp = UserDataSchema().load(Helpers().UserDataJSONFactory(id="example_user"))
    temp.monitors.append(example_monitor_job)

    return temp

@pytest.fixture
def example_empty_user_data():
    return UserDataSchema().load(Helpers().UserDataJSONFactory(id="example_user"))

@pytest.fixture
def example_monitor_job():
    return MonitorJobSchema().load(Helpers().MonitorJobJSONFactory())

@pytest.fixture
def example_empty_user_data_json():
    return Helpers().UserDataJSONFactory(id="example_user")

@pytest.fixture
def example_monitor_job_json():
    return Helpers().MonitorJobJSONFactory()


class Helpers:
    @staticmethod
    def UserDataJSONFactory(*, id, monitors=[]):
        return {"id": id, "monitors": monitors}

    @staticmethod
    def MonitorJobJSONFactory(
        *,
        id=1,
        make_screenshots=True,
        sleep_time=1,
        url="http://example.com",
    ):
        return {
            "id": id,
            "makeScreenshots": make_screenshots,
            "sleepTime": sleep_time,
            "url": url,
        }


@pytest.fixture
def helpers():
    return Helpers
