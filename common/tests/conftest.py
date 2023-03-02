import pytest

_EXAMPLE_USER_EMAIL = "user@example.com"
_EXAMPLE_USER_ID = "unique-user-id"


class Helpers:
    @staticmethod
    def scheduled_job_dict_factory(
        *,
        user_email=_EXAMPLE_USER_EMAIL,
        user_id=_EXAMPLE_USER_ID,
        job_id=1,
        sleep_time=1,
    ):
        return {
            "user_email": user_email,
            "user_id": user_id,
            "job_id": job_id,
            "sleep_time": sleep_time,
        }

    @staticmethod
    def test_job_dict_factory(*args, **kwargs):
        temp = Helpers.scheduled_job_dict_factory(*args, **kwargs)
        return temp


@pytest.fixture(name="helpers")
def helpers_fixture():
    return Helpers


@pytest.fixture()
def example_user_email():
    return _EXAMPLE_USER_EMAIL


@pytest.fixture()
def example_user_id():
    return _EXAMPLE_USER_ID
