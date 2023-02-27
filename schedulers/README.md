# Schedulers

The scope of this project is to react to `SchedulerChangeEvent`s coming via the input SQS queue
and modify the corresponding EventBridge Schedulers.

Scheduler's name is provided as part of the input event, similarly the operation to run on it, which can be one of:

- CREATE
- MODIFY
- REMOVE

# Configuration (env variables)

- `DISTRIBUTION_SNS_TOPIC_ARN` - what topic should the schedulers emit events to
- `SCHEDULERS_GROUP` - what group should the schedulers be assigned to. This should be equal to prefix of the deployment in most cases
- `SCHEDULERS_ROLE_ARN` - ARN of the role that allows for `sns:Publish` to the above mentioned SNS. This role is to be used by the concrete schedulers

# TODO:

There are no proper tests for the logic, as `moto` does not seem to support EventBridge Scheduler at the time of writing
