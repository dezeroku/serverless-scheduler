# Page Monitor

AWS based serverless solution to monitor websites for changes in HTML.
When such a change is detected user is notified via mail.

## Why?

I've written it for myself and use it for monitoring couple pages, but the main idea behind it was to get a practical grasp on the microservices and cloud (AWS in this case).

## How does it look?

Couple screenshots from the `front` provided UI.

![Home Page (empty)](docs/static/front/home.png?raw=true "Home Page (empty)")
![Task Creation](docs/static/front/create.png?raw=true "Task Creation")
![Home Page](docs/static/front/added.png?raw=true "Home Page")
![Modify Modal](docs/static/front/modify.png?raw=true "Modify Modal")

## Top level design

- Frontend - React
- CRUD - api-gateway + Lambdas on backend, writing to `Items` dynamodb
- Dynamodb Streams - reading changes in `Items` DB and passing these to FIFO SQS `item-changes` (to not block)
- FIFO SQS `item-changes` consumer, owning a set of EventBridge Schedulers that are modified according to incoming DB changes
- EventBridge Schedulers inserting events to an SNS `Distribution`
- SQSs attached to SNS `Distribution` getting the produced events from `Distribution` SNS based on event type (e.g. html handler vs checking port on some host being open handler)
- Finally real "checker" lambdas consuming events from SQSs (keeping temporary state in S3)
- Real "checker" lambdas inserting the (potential) notification events to `Output` SQS (or should it be SNS)
- `Output` events are consumed by a Lambda reponsible for outgoing communication

### Why so many levels?

To make it as asynchronous as possible

### Potential dangers

- EventBridge Schedulers getting out of sync with `Items` DB - is it possible?

## Structure (AWS refactored)

Let me shed some light on the general design and describe the more important ones.
Each of the modules listed below is stored in a separate directory with its own README listing possible configuration options.
If the component exposes an API, there is a swagger file describing it in the appropriate directory.
The only components that are meant to be exposed to the outside world at any point are `manager` and `front`.

At the moment, the whole deployment consists of few modules that are required, such as:

- manager
- sender

and few optional ones:

- front
- db (this is a rather special case in terms of "being optional", you are still going to have the DB if you reject this, but it's going to be sqlite3 local one)
- screenshoter
- comparator

Most of the modules are accessible via the REST API (except for front and db, these are special).

### High level overview

The entry point for a system is `front` + `manager` underneath (manager also in Lambda).
These are responsible for seeding the AWS SQS queue with initial messages + adding entry for these in DynamoDB.
The messages in queue are given delay based on the user input.
When the time comes to process a message, it triggers a Lambda function that:

1. consumes the message from queue
2. obtains a fresh HTML of the website that's being monitored
3. checks if there is a previous entry for the checker (this is done via call to DynamoDB)
4. if there is, compares it with the freshly obtained copy. Depending on the result, mail gets sent to the user or not
5. saves the fresh HTML as previous entry (DynamoDB)
6. pushes the fresh message with the original delay to the "manager" queue (effectively creating the infinite loop of checking, which is stopped
   if the manager sees that the underlying entry does not exist anymore). Can this be done better? Empty the queue from messages on demand?

TODO: authentication via Cognito

So:

1. DynamoDB for storing user defined websites to monitor and details
2. DynamoDB (or maybe S3?) for "session" storage of HTML (and screenshots, this definitely sounds like S3)
3. SQS for messages "to be checked" to be worked by checkers (in batches)
4. SQS for messages "to be confirmed" to be worked by orchestrator (if the request is still valid, it gets to the "to be checked" queue) in batches. Can this be simplified?
   This is something new, it was part of the `manager` in original approach.
5. Cognito for authorisation
6. still sendgrid for mails for now?
7. Manager has to be "lambdadized"

We don't really have to care about being in sync here (potential issues with front displaying proper state?).

In the overview above, screenshots can also be taken and kept alongside the HTML code, although it significantly affects the running time.

So to sumarize:

- Adding the website to the monitored list, seeds the queue with initial message
- Removing the website from monitored list, removes all the related messages from the queue

This should eliminate the need of sanity checking the queue (what about possible race conditions though?).

### Manager

That's the core part of the system.
It's meant to keep the user list and control (spin up and terminate) the `checker` queue.
It's possible to use it with the local `sqlite3` db or connect to `postgres` (the so-called `db` module).

### Sender

Responsible for contacting with the outside world.
For now only one API call that matters (`mail`), that uses the `sendgrid` API under the hood.

### Front

UI that contacts with the `manager` over the API.
That's the entry point, if you don't want to use the API directly.

### Screenshoter

Takes a screenshot of the provided URL.
Under the hood it's using `puppeteer`.

### Comparator

Provided with two images it calculates the structural similarity (basically a diff value) between these two.
It's used to mark the borders of what changed between the checks.

### Checker

Shouldn't be used directly at any point.
It's the smallest component actually responsible for calling the other services.
It's given a single URL to check and periodically compares an HTML diff between the previous and current content.
In case of any difference, it sends out a mail informing about the change.

## Deployment

TBA

## Building

TBA for the Lambda case

All of the images are provided under the `ghcr.io/dezeroku` namespace and are automatically rebuilt on every change in the `master` branch of the repo.

Each of the components can be built via the provided Dockerfile.
To get the production build:

```
# Skip the test stages with proper runner
export DOCKER_BUILDKIT=1
docker build -t production .
```

To run tests:

```
docker build -t test . --target test
docker run -it test
```

## Utilities

The `utils` directory contains few useful scripts that can be used in CI or just to speed-up the development.

- `create_schemas.sh` -> generates `common/common_schemas.py` (contain JSON schemas) based on the `swagger/swagger.yaml`. The schemas are used later on in handler to validate requests/responses
- `deploy.sh` -> small wrapper, does the necessary calls to deploy whole application to AWS
- `teardown.sh` -> small wrapper, does the necessary calls to remove whole application from AWS
- `json2py.py` -> utility for `create_schemas.sh`, converts .json files to .py file, which has a single variable inside and its value is the original .json content

## Ideas

Two queues, `schedulers` responsible for inserting jobs (based on sleepTime) and `monitors` which actually visit the website and compare with previous state.

Or should I just merge these into a single `monitors`?

# How to deploy it?

First build the packages by issuing

```
./utils/build.sh FULL
```

then prepare the `<ENV>-secret-values.tfvars` in `terraform/deployments/core` (you can base on `dev-secret-values.tfvars.example` and finally

```
DEPLOY_ENV=<ENV> ./utils/deploy.sh FULL
```
