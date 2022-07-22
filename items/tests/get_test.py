from common import utils
from items.get import handler
from items.models import MonitorJob, UserData
from items.schemas import MonitorJobSchema, UserDataSchema


def test_initial_data_addition(empty_mock_db, table_name):
    user = "non-existing-user"
    table = empty_mock_db.Table(table_name)

    # Make sure that item does not exist
    try:
        table.get_item(Key={"id": user})
        assert False
    except:
        pass

    response = handler(table, user)

    result = table.get_item(Key={"id": user})["Item"]
    user_data_fetched = UserDataSchema().load(result)

    assert response == user_data_fetched.monitors
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
