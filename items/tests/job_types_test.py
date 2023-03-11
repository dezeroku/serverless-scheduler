import json

from serverless_scheduler_plugin_example_api.models.test_job import TestJob

from items.job_types import get, handler


def test_job_types_get():
    job_types = handler()

    assert job_types == [TestJob.schema()]


def test_job_types_get_event():
    result = get(None, None)

    assert result.get("statusCode") == 200  # pylint: disable=no-member

    job_types = json.loads(result.get("body"))  # pylint: disable=no-member

    assert job_types == [TestJob.schema()]
