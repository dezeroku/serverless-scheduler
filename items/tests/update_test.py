import copy

import pytest

from common.models.plugins import parse_dict_to_job
from items.update import handler, update


@pytest.fixture(autouse=True)
def setup(helpers, mock_db_table, db_user):
    # Add a single element to DB to be used later on in tests
    monitor_job = parse_dict_to_job(
        helpers.test_job_dict_factory(user_id=db_user, job_id=0)
    )

    to_save = monitor_job.dict()
    mock_db_table.put_item(Item=to_save)


def test_successful_update(mock_db_table, db_user, db_user_email, helpers):
    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    old_item = parse_dict_to_job(monitor_jobs_dicts[0])
    job_id = old_item.job_id

    new_item = copy.deepcopy(old_item)
    new_item.sleep_time = old_item.sleep_time + 1

    assert new_item.sleep_time != old_item.sleep_time

    payload = new_item.dict()

    response = handler(mock_db_table, db_user_email, db_user, job_id, payload)

    assert response["statusCode"] == 200

    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    changed = parse_dict_to_job(monitor_jobs_dicts[0])
    assert changed == new_item


def test_successful_update_event(
    helpers, monkeypatch, table_name, mock_db_table, db_user, db_user_email
):
    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    old_item = parse_dict_to_job(monitor_jobs_dicts[0])
    job_id = old_item.job_id

    new_item = copy.deepcopy(old_item)
    new_item.sleep_time = old_item.sleep_time + 1

    assert new_item.sleep_time != old_item.sleep_time

    payload = new_item.dict()

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        body=payload,
        cognitoUsername=db_user,
        cognitoEmail=db_user_email,
        pathParameters={"job_id": job_id},
    )
    context = None
    response = update(event, context)

    assert response["statusCode"] == 200

    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    changed = parse_dict_to_job(monitor_jobs_dicts[0])
    assert changed == new_item


def test_update_nonexisting(mock_db_table, db_user_email, db_user, helpers):
    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    old_item = parse_dict_to_job(monitor_jobs_dicts[0])
    job_id = old_item.job_id + 1

    payload = old_item.dict()

    response = handler(mock_db_table, db_user_email, db_user, job_id, payload)

    assert response["statusCode"] == 404

    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1
    assert parse_dict_to_job(monitor_jobs_dicts[0]) == old_item


def test_update_nonexisting_event(
    helpers, monkeypatch, table_name, mock_db_table, db_user, db_user_email
):
    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1

    old_item = parse_dict_to_job(monitor_jobs_dicts[0])

    job_id = old_item.job_id + 1

    payload = old_item.dict()

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        body=payload,
        cognitoUsername=db_user,
        cognitoEmail=db_user_email,
        pathParameters={"job_id": job_id},
    )
    context = None
    response = update(event, context)

    assert response["statusCode"] == 404

    monitor_jobs_dicts = helpers.get_monitor_jobs_for_user(mock_db_table, db_user)
    assert len(monitor_jobs_dicts) == 1
    assert parse_dict_to_job(monitor_jobs_dicts[0]) == old_item
