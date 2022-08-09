import json

from common import utils
from items.get import get, handler
from items.models import MonitorJob, UserData
from items.schemas import MonitorJobSchema, UserDataSchema


def test_initial_data_addition(empty_mock_db, table_name):
    user = "non-existing-user"
    table = empty_mock_db.Table(table_name)

    # Make sure that item does not exist
    result = table.get_item(Key={"id": user})
    if "Item" in result:
        assert False

    response = handler(table, user)

    result = table.get_item(Key={"id": user})["Item"]
    user_data_fetched = UserDataSchema().load(result)

    assert response == user_data_fetched.monitors
    assert user_data_fetched.id == user
    assert not user_data_fetched.monitors


def test_initial_data_addition_event(helpers, monkeypatch, empty_mock_db, table_name):
    user = "non-existing-user"
    table = empty_mock_db.Table(table_name)

    # Make sure that item does not exist
    result = table.get_item(Key={"id": user})
    if "Item" in result:
        assert False

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(cognitoUsername=user)
    context = None
    response = get(event, context)

    result = table.get_item(Key={"id": user})["Item"]
    user_data_fetched = UserDataSchema().load(result)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == user_data_fetched.monitors
    assert user_data_fetched.id == user
    assert not user_data_fetched.monitors


def test_data_fetch_empty(empty_mock_db, table_name):
    user = "existing-user"
    table = empty_mock_db.Table(table_name)

    user_data = UserDataSchema().load({"id": user})
    to_save = UserDataSchema().dump(user_data)
    table.put_item(Item=to_save)

    response = handler(table, user)

    assert response == user_data.monitors
    assert not response


def test_data_fetch_empty_event(helpers, monkeypatch, empty_mock_db, table_name):
    user = "existing-user"
    table = empty_mock_db.Table(table_name)

    user_data = UserDataSchema().load({"id": user})
    to_save = UserDataSchema().dump(user_data)
    table.put_item(Item=to_save)

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(cognitoUsername=user)
    context = None
    response = get(event, context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == user_data.monitors
    assert not json.loads(response["body"])


def test_data_fetch_single_item(empty_mock_db, table_name):
    user = "existing-user"
    table = empty_mock_db.Table(table_name)

    monitor = MonitorJob(12, True, 5, "http://example.com")
    user_data = UserData(user, [monitor])

    to_save = UserDataSchema().dump(user_data)
    table.put_item(Item=to_save)

    response = handler(table, user)

    dumped = MonitorJobSchema(many=True).dump(user_data.monitors)

    assert response == utils.replace_decimals(dumped)


def test_data_fetch_single_item_event(helpers, monkeypatch, empty_mock_db, table_name):
    user = "existing-user"
    table = empty_mock_db.Table(table_name)

    monitor = MonitorJob(12, True, 5, "http://example.com")
    user_data = UserData(user, [monitor])

    to_save = UserDataSchema().dump(user_data)
    table.put_item(Item=to_save)

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(cognitoUsername=user)
    context = None
    response = get(event, context)

    dumped = MonitorJobSchema(many=True).dump(user_data.monitors)

    assert json.loads(response["body"]) == utils.replace_decimals(dumped)
    assert response["statusCode"] == 200
