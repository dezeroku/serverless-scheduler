import copy

import pytest

from common import utils
from items.models import MonitorJob, UserData
from items.schemas import MonitorJobSchema, UserDataSchema
from items.update import handler


@pytest.fixture(autouse=True)
def setup(mock_db_table, db_user):
    # Add a single element to DB to be used later on in tests
    monitor = MonitorJob(12, True, 5, "http://example.com")
    user_data = UserData(db_user, [monitor])

    to_save = UserDataSchema().dump(user_data)
    mock_db_table.put_item(Item=to_save)


def test_successful_update(mock_db_table, db_user):
    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1

    old_item = loaded.monitors[0]
    item_id = old_item.id

    new_item = copy.deepcopy(old_item)
    new_item.sleep_time = old_item.sleep_time + 1
    new_item.make_screenshots = not old_item.make_screenshots

    assert new_item.sleep_time != old_item.sleep_time
    assert new_item.make_screenshots != old_item.make_screenshots

    payload = MonitorJobSchema().dump(new_item)

    response = handler(mock_db_table, db_user, item_id, payload)

    assert response["statusCode"] == 200

    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    changed = loaded.monitors[0]

    assert changed == new_item


def test_update_nonexisting(mock_db_table, db_user):
    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1

    old_item = loaded.monitors[0]
    item_id = old_item.id + 1

    payload = MonitorJobSchema().dump(old_item)

    response = handler(mock_db_table, db_user, item_id, payload)

    assert response["statusCode"] == 404

    user_data = mock_db_table.get_item(Key={"id": db_user})["Item"]
    loaded = UserDataSchema().load(user_data)

    assert len(loaded.monitors) == 1
    assert loaded.monitors[0] == old_item
