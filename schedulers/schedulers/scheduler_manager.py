# TODO: Sadly no tests for this yet
# as moto doesn't support EventBridge Scheduler at the time this is being written

import math
from typing import TYPE_CHECKING

from common.models.jobs import ScheduledJob

if TYPE_CHECKING:
    from mypy_boto3_scheduler import EventBridgeSchedulerClient
else:
    EventBridgeSchedulerClient = object


class SchedulerManager:
    """
    Simple wrapper that controls EventBridge Scheduler state
    """

    # TODO: do we really case what ScheduledJob is?
    # This could be made more generic, just getting any str to pass further on
    # On the other hand, it's always nice to revalidate
    def __init__(
        self,
        client: EventBridgeSchedulerClient,
        scheduler_group: str,
        scheduler_id: str,
        job_config: ScheduledJob = None,
    ):
        self.client = client
        self.scheduler_group = scheduler_group
        self.scheduler_id = scheduler_id
        self.job_config = job_config

    def _modify_in_aws(self, method, target_sns_arn, target_sns_role):
        # Create and update take the same parameters
        # Update overrides the state with default values if not provided
        # Thus use a common helper to make sure the params are the same between creation and update
        method(
            GroupName=self.scheduler_group,
            Name=self.scheduler_id,
            FlexibleTimeWindow={"Mode": "OFF"},
            ScheduleExpression=SchedulerManager.get_schedule_expression(
                self.job_config
            ),
            Target={
                "Arn": target_sns_arn,
                "RoleArn": target_sns_role,
                "Input": self.job_config.json(),
            },
        )

    def create(self, target_sns_arn: str, target_sns_role: str):
        self._modify_in_aws(
            self.client.create_schedule, target_sns_arn, target_sns_role
        )

    def update(self, target_sns_arn: str, target_sns_role: str):
        # There's no check in place to avoid updates that don't check the state
        # It's cheaper to just call the update function than add custom check
        # logic and increase run time
        self._modify_in_aws(
            self.client.update_schedule, target_sns_arn, target_sns_role
        )

    def delete(self):
        self.client.delete_schedule(
            GroupName=self.scheduler_group, Name=self.scheduler_id
        )

    @staticmethod
    def get_schedule_expression(job_config: ScheduledJob):
        if (sleep_time := job_config.sleep_time) < 1:
            raise ValueError("sleep_time must be at least 1 second")

        # Round up to full minutes, as the time provided is in seconds
        if (sleep_time_minutes := math.ceil(sleep_time / 60)) == 1:
            return "rate(1minute)"

        return f"rate({sleep_time_minutes}minutes)"
