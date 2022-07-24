import pytest
from marshmallow.exceptions import ValidationError

from items.models import MonitorJob, UserData
from items.schemas import MonitorJobSchema, UserDataSchema

# TODO: Make the tests below work with fixture definitions from conftest
# def example_empty_user_data_json(helpers):
#    return helpers.UserDataJSONFactory(id="example_user")
#
#
# def example_monitor_job_json(helpers):
#    return helpers.MonitorJobJSONFactory()
#
#
# @pytest.mark.parametrize("in_data",
#                         [
#                             example_monitor_job_json(),
#                             example_empty_user_data_json()
#                         ])
# @pytest.mark.parametrize(
#    "schema, cls",
#    [
#        (MonitorJobSchema(), MonitorJob),
#        (UserDataSchema(), UserData),
#    ],
# )
# def test_schema_load_to_object(in_data, schema, cls):
#    assert isinstance(schema.load(in_data), cls)
#
#
# @pytest.mark.parametrize("in_data",
#                         [
#                             example_monitor_job_json(),
#                             example_empty_user_data_json()
#                         ])
# @pytest.mark.parametrize(
#    "schema",
#    [
#        (MonitorJobSchema()),
#        (UserDataSchema()),
#    ],
# )
# def test_schema_dump(in_data, schema):
#    data = schema.load(in_data)
#    dumped = schema.dump(data)
#
#    assert dumped == in_data


@pytest.mark.parametrize(
    "in_data",
    [
        {
            "id": 1,
            "make_screenshots": True,
            "sleep_time": 1,
            "url": "broken-url",
        }
    ],
)
def test_monitor_job_schema_load_url_validates(in_data, helpers):
    schema = MonitorJobSchema()
    try:
        assert schema.load(helpers.MonitorJobJSONFactory(**in_data))
        assert False
    except ValidationError as e:
        assert "Not a valid URL" in str(e)


@pytest.mark.parametrize(
    "in_data",
    [
        {
            "id": 1,
            "make_screenshots": True,
            "sleep_time": -1,
            "url": "http://example.com",
        }
    ],
)
def test_monitor_job_schema_load_negative_sleep_time_error(in_data, helpers):
    schema = MonitorJobSchema()
    try:
        assert schema.load(helpers.MonitorJobJSONFactory(**in_data))
        assert False
    except ValidationError as e:
        assert "sleepTime must be a positive number" in str(e)
