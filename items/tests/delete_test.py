import pytest

from common import utils
from items.delete import delete, handler
from items.models import MonitorJob, UserData
from items.schemas import MonitorJobSchema, UserDataSchema


@pytest.fixture(autouse=True)
def setup(mock_db_table, db_user):
    # Add a single element to DB to be used later on in tests
    monitor = MonitorJob(12, True, 5, "http://example.com")
    user_data = UserData(db_user, [monitor])

    to_save = UserDataSchema().dump(user_data)
    mock_db_table.put_item(Item=to_save)


def test_successful_delete(mock_db_table, db_user):
    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1

    item_id = loaded.monitors[0].id

    response = handler(mock_db_table, db_user, item_id)

    assert response["statusCode"] == 200

    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 0


def test_successful_delete_event(
    monkeypatch, helpers, table_name, mock_db_table, db_user
):
    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1

    item_id = loaded.monitors[0].id

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        cognitoUsername=db_user, pathParameters={"item_id": item_id}
    )
    context = None
    response = delete(event, context)

    assert response["statusCode"] == 200

    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 0


def test_delete_nonexisting(mock_db_table, db_user):
    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1

    item_id = loaded.monitors[0].id + 1

    response = handler(mock_db_table, db_user, item_id)

    assert response["statusCode"] == 404

    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1


def test_delete_nonexisting_event(
    monkeypatch, helpers, table_name, mock_db_table, db_user
):
    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1

    item_id = loaded.monitors[0].id + 1

    monkeypatch.setenv("DYNAMO_DB", table_name)
    event = helpers.EventFactory(
        cognitoUsername=db_user, pathParameters={"item_id": item_id}
    )
    context = None
    response = delete(event, context)

    assert response["statusCode"] == 404

    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1
