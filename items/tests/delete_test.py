import pytest

from common.models import HTMLMonitorJob
from items.delete import delete, handler


@pytest.fixture(autouse=True)
def setup(mock_db_table, helpers):
    # Add a single element to DB to be used later on in tests
    monitor_job = helpers.html_monitor_job_dict_factory(job_id=123)

    to_save = HTMLMonitorJob(**monitor_job).dict()
    mock_db_table.put_item(Item=to_save)


def test_successful_delete(mock_db_table, db_user, helpers):
    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    monitor_job_id = HTMLMonitorJob(**monitor_jobs_dicts[0]).job_id

    response = handler(mock_db_table, db_user, monitor_job_id)

    assert response["statusCode"] == 200

    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 0


def test_successful_delete_event(
    monkeypatch, helpers, table_name, mock_db_table, db_user, db_user_email
):
    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    monitor_job_id = HTMLMonitorJob(**monitor_jobs_dicts[0]).job_id

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        cognitoUsername=db_user,
        cognitoEmail=db_user_email,
        pathParameters={"job_id": monitor_job_id},
    )
    context = None
    response = delete(event, context)

    assert response["statusCode"] == 200

    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 0


def test_delete_nonexisting(mock_db_table, db_user, helpers):
    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    nonexistent_monitor_job_id = HTMLMonitorJob(**monitor_jobs_dicts[0]).job_id + 1

    response = handler(mock_db_table, db_user, nonexistent_monitor_job_id)

    assert response["statusCode"] == 404

    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1


def test_delete_nonexisting_event(
    monkeypatch, helpers, table_name, mock_db_table, db_user, db_user_email
):
    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    nonexistent_monitor_job_id = HTMLMonitorJob(**monitor_jobs_dicts[0]).job_id + 1

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        cognitoUsername=db_user,
        cognitoEmail=db_user_email,
        pathParameters={"job_id": nonexistent_monitor_job_id},
    )
    context = None
    response = delete(event, context)

    assert response["statusCode"] == 404

    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1
