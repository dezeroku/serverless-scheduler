import pytest
from boto3.dynamodb.conditions import Key

from items.delete import delete, handler
from items.models import MonitorJob


@pytest.fixture(autouse=True)
def setup(mock_db_table, db_user, helpers):
    # Add a single element to DB to be used later on in tests
    monitor_job = helpers.MonitorJobJSONFactory(job_id=123)

    to_save = MonitorJob(**monitor_job).dict()
    mock_db_table.put_item(Item=to_save)


def test_successful_delete(mock_db_table, db_user):
    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_email").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    monitor_job_id = MonitorJob(**monitor_jobs_dicts[0]).job_id

    response = handler(mock_db_table, db_user, monitor_job_id)

    assert response["statusCode"] == 200

    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_email").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 0


def test_successful_delete_event(
    monkeypatch, helpers, table_name, mock_db_table, db_user
):
    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_email").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    monitor_job_id = MonitorJob(**monitor_jobs_dicts[0]).job_id

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        cognitoEmail=db_user, pathParameters={"item_id": monitor_job_id}
    )
    context = None
    response = delete(event, context)

    assert response["statusCode"] == 200

    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_email").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 0


def test_delete_nonexisting(mock_db_table, db_user):
    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_email").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    nonexistent_monitor_job_id = MonitorJob(**monitor_jobs_dicts[0]).job_id + 1

    response = handler(mock_db_table, db_user, nonexistent_monitor_job_id)

    assert response["statusCode"] == 404

    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_email").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1


def test_delete_nonexisting_event(
    monkeypatch, helpers, table_name, mock_db_table, db_user
):
    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_email").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1

    nonexistent_monitor_job_id = MonitorJob(**monitor_jobs_dicts[0]).job_id + 1

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        cognitoEmail=db_user, pathParameters={"item_id": nonexistent_monitor_job_id}
    )
    context = None
    response = delete(event, context)

    assert response["statusCode"] == 404

    monitor_jobs_dicts = mock_db_table.query(
        KeyConditionExpression=Key("user_email").eq(db_user)
    )["Items"]
    assert len(monitor_jobs_dicts) == 1
