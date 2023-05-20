# Architecture

![Architecture](docs/diagrams/created/high_level_overview.png?raw=true "High Level Overview")

There are few packages worth mentioning that together make the system work:

1. `common` package which defines the schemas for all the communication between services
2. `items` microservice, which exposes REST API and accepts objects that match `ScheduledJob` definitions from `common`.
   The data is then kept in DynamoDB
3. `front`end for the above API
4. `schedulers` which monitor the DynamoDB changes and manages schedulers that periodically issue events to an SNS topic.
5. [plugins/serverless-scheduler-html-checker](http://github.com/dezeroku/serverless-scheduler-html-checker) which is an example implementation of an SNS topic listener (it only collects events that match `job_type=='html_monitor_job'`).
   Based on this one you can write your own checkers that do whatever you want
