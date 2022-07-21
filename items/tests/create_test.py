from items.create import generate_next_id, get_monitor_job_with_id

# TODO: The cases below should be also parametrized with pytest.mark.parametrize
# but they use fixtures
def test_generate_next_id_empty(example_empty_user_data):
    assert generate_next_id(example_empty_user_data) == 1

def test_generate_next_id(example_user_data):
    assert generate_next_id(example_user_data) == 2

def test_get_monitor_job_with_id(example_monitor_job_json):
    temp = get_monitor_job_with_id(example_monitor_job_json, 5)
    assert temp.id == 5
