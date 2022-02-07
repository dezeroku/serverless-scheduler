# Page Monitor (monitor-page)
AWS based solution to monitor websites for changes in either HTML or screenshots of them.
When such a change is detected user is notified via mail.

## Why?
I've written it for myself and use it for monitoring couple pages, but the main idea behind it was to get a practical grasp on the microservices and cloud (AWS in this case).
That's why the components are split as much as possible.
The similar approach would be probably to just use a message-broker such as `RabbitMQ` instead of running a new checker lambda function for every URL.
I haven't really compared it cost-wise yet though.

## How does it look?
Couple screenshots from the `front` provided UI.

![Login](docs/pictures/login.png?raw=true "Login")
![Home Page (empty)](docs/pictures/home.png?raw=true "Home Page (empty)")
![Task Creation](docs/pictures/create.png?raw=true "Task Creation")
![Home Page](docs/pictures/added.png?raw=true "Home Page")
![Modify Modal](docs/pictures/modify.png?raw=true "Modify Modal")

## Structure (AWS refactored)

Let me shed some light on the general design and describe the more important ones.
Each of the modules listed below is stored in a separate directory with its own README listing possible configuration options.
If the component exposes an API, there is a swagger file describing it in the appropriate directory.
The only components that are meant to be exposed to the outside world at any point are `manager` and `front`.

At the moment, the whole deployment consists of few modules that are required, such as:
* manager
* sender

and few optional ones:
* front
* db (this is a rather special case in terms of "being optional", you are still going to have the DB if you reject this, but it's going to be sqlite3 local one)
* screenshoter
* comparator

Most of the modules are accessible via the REST API (except for front and db, these are special).

### High level overview
The entry point for a system is `front` + `manager` underneath.
These are responsible for seeding the AWS SQS queue with initial messages.
The messages in queue are given delay based on the user input (kept in `db` stored in S3).
When the time comes to process a message, it triggers a Lambda function that:
1. consumes the message from queue
2. obtains a fresh HTML of the website that's being monitored
3. checks if there is a previous entry for the checker
4. if there is, compares it with the freshly obtained copy. Depending on the result, mail gets sent to the user or not
5. saves the fresh HTML as previous entry
6. pushes the fresh message with the original delay back to the queue (effectively creating the infinite loop of checking)

In the overview above, screenshots can also be taken and kept alongside the HTML code, although it significantly affects the running time.

So to sumarize:
* Adding the website to the monitored list, seeds the queue with initial message
* Removing the website from monitored list, removes all the related messages from the queue

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
