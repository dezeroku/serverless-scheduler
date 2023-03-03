import json

from common.models.plugins import parse_dict_to_job
from items import utils
from items.get import get, handler


def test_data_fetch_empty(empty_mock_db, table_name, db_user):
    table = empty_mock_db.Table(table_name)

    response = handler(table, db_user)

    assert response == []


def test_data_fetch_empty_event(
    helpers, monkeypatch, empty_mock_db, table_name, db_user, db_user_email
):
    empty_mock_db.Table(table_name)

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(cognitoEmail=db_user_email, cognitoUsername=db_user)
    context = None
    response = get(event, context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == []


def test_data_fetch_single_item(empty_mock_db, table_name, db_user, helpers):
    table = empty_mock_db.Table(table_name)

    monitor_job = parse_dict_to_job(
        helpers.html_monitor_job_dict_factory(user_id=db_user)
    )

    to_save = monitor_job.dict()
    table.put_item(Item=to_save)

    response = handler(table, db_user)

    dumped = [monitor_job.dict()]
    assert response == utils.replace_decimals(dumped)


def test_data_fetch_single_item_event(
    helpers, monkeypatch, empty_mock_db, table_name, db_user, db_user_email
):
    table = empty_mock_db.Table(table_name)

    monitor_job = parse_dict_to_job(
        helpers.html_monitor_job_dict_factory(user_id=db_user)
    )

    to_save = monitor_job.dict()
    table.put_item(Item=to_save)

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(cognitoEmail=db_user_email, cognitoUsername=db_user)
    context = None
    response = get(event, context)

    assert response["statusCode"] == 200

    dumped = [monitor_job.dict()]
    assert json.loads(response["body"]) == utils.replace_decimals(dumped)


# These tests take a long time and aren't really worth the hassle to run them
# TODO: Is there a simpler way to test pagination?
# def test_data_fetch_pagination_fail(empty_mock_db, table_name, db_user, helpers):
#    table = empty_mock_db.Table(table_name)
#
#    monitor_job = MonitorJob(
#        **helpers.html_monitor_job_dict_factory(user_email=db_user, job_id=0)
#    )
#    for i in range(13000):
#        monitor_job.job_id = i
#        to_save = monitor_job.dict()
#        table.put_item(Item=to_save)
#
#    response = handler(table, db_user, pagination=False)
#
#    assert len(response) != 13000
#
#
# def test_data_fetch_pagination_works(empty_mock_db, table_name, db_user, helpers):
#    table = empty_mock_db.Table(table_name)
#
#    monitor_job = MonitorJob(
#        **helpers.html_monitor_job_dict_factory(user_email=db_user, job_id=0)
#    )
#    for i in range(13000):
#        monitor_job.job_id = i
#        to_save = monitor_job.dict()
#        table.put_item(Item=to_save)
#
#    response = handler(table, db_user)
#
#    assert len(response) == 13000
