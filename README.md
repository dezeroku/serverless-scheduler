# Serverless Scheduler

[![Tests and packaging](https://github.com/dezeroku/serverless-scheduler/actions/workflows/flow.yml/badge.svg)](https://github.com/dezeroku/serverless-scheduler/actions/workflows/flow.yml)

AWS based serverless solution for scheduling tasks.

If your workflow fits the generic "every `n` minutes do `something`" and you're willing to implement a plugin for `something` then this project will cover "every `n` minutes" part for you and provide you with UI for setting up individual jobs.

I mostly use it for website change detection, however it's easy to extend it with plugins that can be implemented to do whatever you like.

The API and scheduler core are pretty stable as of now, but the frontend requires a rewrite (to properly get supported job types that were added as a plugin).

In reality if you don't need it to scale to the moon or support multiple "tasks" types then your best bet is to use a widely recognized project such as [changedetection.io](https://github.com/dgtlmoon/changedetection.io).

# Pointers

- [How to deploy it?](docs/md/deployments.md)
- [How does it look?](docs/md/screenshots.md)
- [Plugins](docs/md/plugins.md)
- [Read about architecture](docs/md/architecture.md)

# Architecture Diagram

![Architecture](docs/diagrams/created/high_level_overview.png?raw=true "High Level Overview")

# Honorable mention

For a similar thing but hardcoded to just HTTP monitoring jobs and deployable in Kubernetes cluster look at [the old monitor-page repo](https://github.com/dezeroku/monitor-page).
It is actually an original implementation of the idea.
