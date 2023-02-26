# Schedulers

The scope of this project is to react to `SchedulerChangeEvent`s coming via the input SQS queue
and modify the corresponding EventBridge Schedulers.

Scheduler's name is provided as part of the input event, similarly the operation to run on it, which can be one of:

- CREATE
- MODIFY
- REMOVE

# Configuration (env variables)

- `DISTRIBUTION_SNS_TOPIC_ARN` - what topic should the schedulers emit events to
