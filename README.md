# Page Monitor

AWS based serverless solution for running scheduled tasks coming from different sources.
The main use at the moment is monitoring websites for changes in HTML, however it's easy to extend it with whatever functionality you'd like to have.

The only requirement is for the input JSON to match `ScheduledJob` definition from `common` package + you need to write your handler listening to the events from SNS topic.

This is very much a work in progress at the moment, especially the frontend requires a redesign (to easily allow more job types to be supported).
The scheduling part is done though, it only needs an example HTML monitor listener to be written.

For a similar thing but hardcoded to a single JobType and deployable in Kubernetes cluster look at `k8s` branch of this repo.

In reality if you don't need it to run in a cluster or scale to the moon your best bet is to use a widely recognized project such as [changedetection.io](https://github.com/dgtlmoon/changedetection.io).
Don't use this in production :D

# High level overview

![High Level Overview](docs/diagrams/created/high_level_overview.png?raw=true "High Level Overview")

There are few packages worth mentioning that together make the application:

1. `common` package which defines the schemas for all the communication between services
2. `items` microservice, which exposes REST API and accepts objects that match `ScheduledJob` definitions from `common`.
   The data is then kept in DynamoDB
3. `front`end for the above API
4. `schedulers` which monitors the DynamoDB changes and manages schedulers that periodically issue events to an SNS topic.
5. `html-monitor-implementation` which is an example implementation of an SNS topic listener (it only collects events that match `job_type=='html_monitor_job'`).
   Based on this one you can write your own checkers that do whatever you want

There is probably a bit of over-engineering here, but the idea is to make it as asynchronous as possible and not block at any point.

## Potential dangers

- EventBridge Schedulers getting out of sync with `Items` DB - is it possible?

# How does the frontend look like?

Couple screenshots from the provided web UI.

![Home Page (empty)](docs/static/front/home.png?raw=true "Home Page (empty)")
![Task Creation](docs/static/front/create.png?raw=true "Task Creation")
![Home Page](docs/static/front/added.png?raw=true "Home Page")
![Modify Modal](docs/static/front/modify.png?raw=true "Modify Modal")

# Project layout

There are few "groups" in place.

0. `common` - common definitions to be shared between the python services
1. `items` - REST endpoints for managing scheduled jobs for a user. `terraform/deployments/items-core`
2. `front` - React based UI for the above API. `terraform/deployments/items-front-upload`

# How to deploy it?

## TL;DR

Prepare your own `<DEPLOY_ENV>-secret-values.tfvars` files for directories in `terraform/deployments` and then run

```
./utils/complete_build.sh
./utils/complete_deploy.sh
```

## Deploying specific parts of the system

Each group has its own terraform "blocks", that define parts of the infra.
The are multiple blocks per group, as terraform handles both the core infra (e.g. `items-infra`), but also code deployments (e.g. `items-front-upload`).

Situation is a bit messed up at the moment, but for `items`:

1. There is terraform module for deploying core infra (needs to be run on init)
2. There is terraform module for uploading front files (needs to be run when front changes)
3. There is a terraform module for deploying lambdas and attaching them to API Gateway (needs to be run when backend changes)

First build the packages by issuing

```
./utils/build.sh items
```

then prepare the `<ENV>-secret-values.tfvars` in `terraform/deployments/core` (you can base on `dev-secret-values.tfvars.example` and finally

```
DEPLOY_ENV=<ENV> ./utils/deploy.sh items-infra
DEPLOY_ENV=<ENV> ./utils/deploy.sh items-front-upload
DEPLOY_ENV=<ENV> ./utils/deploy.sh items-lambdas-upload
```

## Plugins

While the core functionality (scheduler + UI) is defined in this repo, handlers for different job types should be kept in `plugins/<specific plugin>` directory, e.g. for `HTMLMonitorJob` consumer there is `plugins/serverless-scheduler-html-checker` directory (git submodule).

These plugins are expected to follow common project structure, so they work seamlessly with existing build system.
Namely:

1. Plugin defines `bin/package_lambda_entrypoint` script, that outputs the zip generated for a project to `.packaging/result/lambda.zip` file. It's up to the developer to define if this script will rely on `serverless-scheduler`'s build system that's used for core packages or define their own logic.
2. Plugin defines `terraform` directory, that contains all the logic needs to deploy the project.
   The following variables should be accepted:
   -. `aws_region` - in what region to deploy
   -. `service` - to be used in tags as 'Service'
   -. `stage` - to be used in tags as 'Stage'
   -. `prefix` - what value to prefix the deployed objects' names with
   -. `lambda_zip_path` - path to zip file that should be used by the consumer Lambda (build system will automatically insert the zip built in step 1.)
   -. `distribution_sns_topic_arn` - ARN of the SNS topic that deployment should monitor for incoming events with matching job_type
   -. `common_layer_arn` - (optional support) ARN of the Lambda layer with `common` package. This is really only usable with Python based plugins

The reference implementation can be seen in abovementioned `plugins/serverless-scheduler-html-checker`.

It's up to the user to define if the consumer should use SQS as a "buffer" before consuming the event by Lambda or not.
In practice the consumer doesn't even have to be a Lambda function, although it's recommended for keeping the whole model serverless.

## TODO

1. Get JobType and job's class definition directly from the plugin, instead of from the `common` package.
   This is basically the last thing (except frontend) that needs to be generalized for the `plugins` to be fully drop-in
