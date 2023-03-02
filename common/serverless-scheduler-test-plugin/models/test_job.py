from common.models import ScheduledJob


class TestJob(ScheduledJob):
    # Dummy job implementation to be used in tests
    # Mark it as non-test
    __test__ = False
