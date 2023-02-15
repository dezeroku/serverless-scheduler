# Page Monitor

AWS based serverless solution for running scheduled tasks coming from different sources.
The main use at the moment is monitoring websites for changes in HTML, where jobs can be set through a provided UI.
When an HTML change is detected user is notified via an email.

This is very much a work in progress at the moment and most of the things don't work (in reality there is only CRUD in place for now).
For a similar thing but working and in K8S look at `k8s` branch of this repo.
In reality if you don't need it to run in a cluster or scale to the moon your best bet is a widely recognized project such as [changedetection.io](https://github.com/dgtlmoon/changedetection.io).
This repo should be treated as a fun project, not something you should rely on.

# High level overview

![High Level Overview](docs/diagrams/created/high_level_overview.png?raw=true "High Level Overview")

- Frontend - React
- CRUD - api-gateway + Lambdas on backend, writing to `Items` dynamodb
- Dynamodb Streams - reading changes in `Items` DB and passing these to FIFO SQS `item-changes` (to not block)
- FIFO SQS `item-changes` consumer, owning a set of EventBridge Schedulers that are modified according to incoming DB changes
- EventBridge Schedulers inserting events to an SNS `Distribution`
- SQSs attached to SNS `Distribution` getting the produced events from `Distribution` SNS based on job type (e.g. html handler vs checking port on some host being open)
- Finally real "checker" lambdas consuming events from SQSs (keeping temporary state in S3 if needed)
- Real "checker" lambdas inserting the (potential) notification events to `Output` SQS (or should it be SNS)
- `Output` events are consumed by a Lambda reponsible for outgoing communication

There is probably a bit of over-engineering here, but the idea is to make it as asynchronous as possible and not block at any point.

## Potential dangers

- EventBridge Schedulers getting out of sync with `Items` DB - is it possible?

# How does the frontend look like?

Couple screenshots from the provided web UI.

![Home Page (empty)](docs/static/front/home.png?raw=true "Home Page (empty)")
![Task Creation](docs/static/front/create.png?raw=true "Task Creation")
![Home Page](docs/static/front/added.png?raw=true "Home Page")
![Modify Modal](docs/static/front/modify.png?raw=true "Modify Modal")

# How to deploy it?

Situation is a bit messed up at the moment, but in general:

1. There is terraform module for deploying core infra
2. There is terraform module for uploading front files
3. Serverless framework is used to deploy functions to API Gateway that's defined in core terraform infra. This is to be rewritten into terraform most likely

First build the packages by issuing

```
./utils/build.sh FULL
```

then prepare the `<ENV>-secret-values.tfvars` in `terraform/deployments/core` (you can base on `dev-secret-values.tfvars.example` and finally

```
DEPLOY_ENV=<ENV> ./utils/deploy.sh FULL
```
