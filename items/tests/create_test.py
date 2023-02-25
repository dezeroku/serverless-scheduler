import json

from common.models import HTMLMonitorJob
from items.create import create, get_monitor_job_with_id, handler


def test_get_monitor_job_with_id(helpers):
    base = helpers.html_monitor_job_dict_factory(job_id=1)
    del base["job_id"]

    result = get_monitor_job_with_id(base, 2)
    assert result.job_id == 2


def test_creation_handler(mock_db, table_name, db_user, helpers):
    to_create = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(
            job_id=None, make_screenshots=True, sleep_time=5, url="http://example.com"
        )
    )

    table = mock_db.Table(table_name)

    payload = to_create.dict()

    response = handler(table, db_user, payload)

    body = response
    assert "job_id" in body
    assert body["job_id"] is not None
    assert isinstance(body["job_id"], int)


def test_double_creation_handler(mock_db, table_name, db_user, helpers):
    to_create = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(
            job_id=None, make_screenshots=True, sleep_time=5, url="http://example.com"
        )
    )

    table = mock_db.Table(table_name)

    payload = to_create.dict()

    response = handler(table, db_user, payload)

    body = response
    assert "job_id" in body
    assert body["job_id"] is not None
    assert isinstance(body["job_id"], int)
    assert body["job_id"] == 0

    # Add second time
    response = handler(table, db_user, payload)

    body = response
    assert body["job_id"] == 1


def test_creation_handler_event(
    helpers, monkeypatch, mock_db, table_name, db_user, db_user_email
):
    to_create = HTMLMonitorJob(
        **helpers.html_monitor_job_dict_factory(
            job_id=None, make_screenshots=True, sleep_time=5, url="http://example.com"
        )
    )

    mock_db.Table(table_name)

    monkeypatch.setenv("DYNAMO_DB", table_name)

    payload = to_create.dict()
    del payload["user_email"]

    event = helpers.EventFactory(
        body=payload, cognitoEmail=db_user_email, cognitoUsername=db_user
    )
    context = None
    response = create(event, context)

    assert response["statusCode"] == 200
    print(response)

    body = json.loads(response["body"])
    assert "job_id" in body
    assert body["job_id"] is not None
    assert isinstance(body["job_id"], int)
