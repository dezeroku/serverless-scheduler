import copy

import pytest
from boto3.dynamodb.conditions import Key

from common import utils
from items.models import MonitorJob
from items.update import handler, update


@pytest.fixture(autouse=True)
def setup(helpers, mock_db_table, db_user):
    # Add a single element to DB to be used later on in tests
    monitor_job = MonitorJob(**helpers.MonitorJobJSONFactory(user_id=db_user, job_id=0))

    to_save = monitor_job.dict()
    mock_db_table.put_item(Item=to_save)


def test_successful_update(mock_db_table, db_user):
    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_id").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    old_item = MonitorJob(**monitor_jobs_dicts[0])
    item_id = old_item.job_id

    new_item = copy.deepcopy(old_item)
    new_item.sleep_time = old_item.sleep_time + 1
    new_item.make_screenshots = not old_item.make_screenshots

    assert new_item.sleep_time != old_item.sleep_time
    assert new_item.make_screenshots != old_item.make_screenshots

    payload = new_item.dict()

    response = handler(mock_db_table, db_user, item_id, payload)

    assert response["statusCode"] == 200

    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_id").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    changed = MonitorJob(**monitor_jobs_dicts[0])
    assert changed == new_item


def test_successful_update_event(
    helpers, monkeypatch, table_name, mock_db_table, db_user
):
    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_id").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    old_item = MonitorJob(**monitor_jobs_dicts[0])
    item_id = old_item.job_id

    new_item = copy.deepcopy(old_item)
    new_item.sleep_time = old_item.sleep_time + 1
    new_item.make_screenshots = not old_item.make_screenshots

    assert new_item.sleep_time != old_item.sleep_time
    assert new_item.make_screenshots != old_item.make_screenshots

    payload = new_item.dict()

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        body=payload, cognitoUsername=db_user, pathParameters={"item_id": item_id}
    )
    context = None
    response = update(event, context)

    assert response["statusCode"] == 200

    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_id").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    changed = MonitorJob(**monitor_jobs_dicts[0])
    assert changed == new_item


def test_update_nonexisting(mock_db_table, db_user):
    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_id").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    old_item = MonitorJob(**monitor_jobs_dicts[0])
    item_id = old_item.job_id + 1

    payload = old_item.dict()

    response = handler(mock_db_table, db_user, item_id, payload)

    assert response["statusCode"] == 404

    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_id").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1
    assert MonitorJob(**monitor_jobs_dicts[0]) == old_item


def test_update_nonexisting_event(
    helpers, monkeypatch, table_name, mock_db_table, db_user
):
    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_id").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    old_item = MonitorJob(**monitor_jobs_dicts[0])
    item_id = old_item.job_id + 1

    payload = old_item.dict()

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        body=payload, cognitoUsername=db_user, pathParameters={"item_id": item_id}
    )
    context = None
    response = update(event, context)

    assert response["statusCode"] == 404

    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_id").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1
    assert MonitorJob(**monitor_jobs_dicts[0]) == old_item
