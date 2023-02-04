import pytest
from moto import mock_dynamodb

from items.create import create, get_monitor_job_with_id, handler
from items.models import MonitorJob


def test_get_monitor_job_with_id(example_monitor_job_json):
    temp = get_monitor_job_with_id(example_monitor_job_json, 5)
    assert temp.job_id == 5


def test_creation_handler(mock_db, table_name, db_user, helpers):
    to_create = MonitorJob(
        **helpers.MonitorJobJSONFactory(
            job_id=None, make_screenshots=True, sleep_time=5, url="http://example.com"
        )
    )

    table = mock_db.Table(table_name)

    payload = to_create.dict()

    response = handler(table, db_user, payload)

    assert response["statusCode"] == 200

    body = response["body"]
    assert "job_id" in body
    assert body["job_id"] is not None
    assert type(body["job_id"]) == int


def test_double_creation_handler(mock_db, table_name, db_user, helpers):
    to_create = MonitorJob(
        **helpers.MonitorJobJSONFactory(
            job_id=None, make_screenshots=True, sleep_time=5, url="http://example.com"
        )
    )

    table = mock_db.Table(table_name)

    payload = to_create.dict()

    response = handler(table, db_user, payload)

    assert response["statusCode"] == 200
    body = response["body"]
    assert "job_id" in body
    assert body["job_id"] is not None
    assert type(body["job_id"]) == int
    assert body["job_id"] == 0

    # Add second time
    response = handler(table, db_user, payload)

    assert response["statusCode"] == 200
    body = response["body"]
    assert body["job_id"] == 1


def test_creation_handler_event(helpers, monkeypatch, mock_db, table_name, db_user):
    to_create = MonitorJob(
        **helpers.MonitorJobJSONFactory(
            job_id=None, make_screenshots=True, sleep_time=5, url="http://example.com"
        )
    )

    table = mock_db.Table(table_name)

    monkeypatch.setenv("DYNAMO_DB", table_name)

    payload = to_create.dict()
    del payload["user_id"]

    event = helpers.EventFactory(body=payload, cognitoUsername=db_user)
    print(event)
    context = None
    response = create(event, context)

    print(response)
    assert response["statusCode"] == 200

    body = response["body"]
    assert "job_id" in body
    assert body["job_id"] is not None
    assert type(body["job_id"]) == int
