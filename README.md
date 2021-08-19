# Page Monitor (monitor-page)
Self hosted k8s solution to monitor websites for changes in either HTML or screenshots of them.
When such a change is detected user is notified via mail.

## Why?
I've written it for myself and use it for monitoring couple pages, but the main idea behind it was to get a grasp on the microservices.
That's why the components are split as much as possible.
The better approach would be probably to just use a message-broker such as `RabbitMQ` instead of running a new checker instance for every URL.

## Structure
Each of the modules listed below is stored in a separate directory with its own README listing possible configuration options.

If the component exposes API, there is a swagger file describing it in the appropriate directory.

| name         | function                                                                                      | type                     | internal / exposed | code    |
| ------------ | --------------------------------------------------------------------------------------------  | ------------------------ | ------------------ | ------- |
| screenshoter | screenshot making container                                                                   | API                      | internal           | Python3 |
| comparator   | picture comparing container - returns diff                                                    | API                      | internal           | Python3 |
| checker      | html checking container                                                                       | worker, no API, no front | internal           | Python3 |
| sender       | sends mesage with data it gets using mail                                                     | API                      | internal           | Python3 |
| manager      | coordinates pods that actually do the checking job, reads/writes db                           | API                      | exposed            | Go      |
| front        | allows user to login based on supported emails and one-time passwords, contacts API, reads DB | front                    | exposed            | React   |
| db           | postgres at the moment, handled with postgres-operator on k8s, stores data                    | DB                       | internal           | N/A     |


## Usage
The manifests which are ready to be deployed on k8s (helm package) are stored in the `k8s/monitor-page` directory.
Requires `postgres-operator` or `local-path-provisioner` to be installed on k8s and configured for the target namespace.

You can run `helm package` in the `k8s/monitor-page` directory to create the package or get it from the "Actions" page from the specific commit.


## Building
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
