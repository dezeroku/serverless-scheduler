import pytest

_EXAMPLE_USER_EMAIL = "user@example.com"


class Helpers:
    @staticmethod
    def scheduled_job_dict_factory(
        *,
        user_email=_EXAMPLE_USER_EMAIL,
        job_id=1,
        sleep_time=1,
    ):
        return {
            "user_email": user_email,
            "job_id": job_id,
            "sleep_time": sleep_time,
        }

    @staticmethod
    def html_monitor_job_dict_factory(
        *,
        user_email=_EXAMPLE_USER_EMAIL,
        job_id=1,
        make_screenshots=True,
        sleep_time=1,
        url="http://example.com",
    ):
        return {
            "user_email": user_email,
            "job_id": job_id,
            "make_screenshots": make_screenshots,
            "sleep_time": sleep_time,
            "url": url,
        }


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture()
def example_user_email():
    return _EXAMPLE_USER_EMAIL
