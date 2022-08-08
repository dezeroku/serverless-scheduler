import pytest
from moto import mock_dynamodb

from items.create import create, generate_next_id, get_monitor_job_with_id, handler
from items.models import MonitorJob
from items.schemas import MonitorJobSchema, UserDataSchema


# TODO: The cases below should be also parametrized with pytest.mark.parametrize
# but they use fixtures
def test_generate_next_id_empty(example_empty_user_data):
    assert generate_next_id(example_empty_user_data) == 1


def test_generate_next_id(example_user_data):
    assert generate_next_id(example_user_data) == 2


def test_get_monitor_job_with_id(example_monitor_job_json):
    temp = get_monitor_job_with_id(example_monitor_job_json, 5)
    assert temp.id == 5


def test_creation_handler(mock_db, table_name, db_user):
    to_create = MonitorJob(
        id=None, make_screenshots=True, sleep_time=5, url="http://example.com"
    )

    table = mock_db.Table(table_name)

    payload = MonitorJobSchema().dump(to_create)

    response = handler(table, db_user, payload)

    assert response["statusCode"] == 200

    body = response["body"]
    assert "id" in body
    assert body["id"] is not None
    assert type(body["id"]) == int


def test_creation_handler_event(helpers, monkeypatch, mock_db, table_name, db_user):
    to_create = MonitorJob(
        id=None, make_screenshots=True, sleep_time=5, url="http://example.com"
    )

    table = mock_db.Table(table_name)

    monkeypatch.setenv("DYNAMO_DB", table_name)

    payload = MonitorJobSchema().dump(to_create)

    event = helpers.EventFactory(body=payload, cognitoUsername=db_user)
    context = None
    response = create(event, context)

    assert response["statusCode"] == 200

    body = response["body"]
    assert "id" in body
    assert body["id"] is not None
    assert type(body["id"]) == int
