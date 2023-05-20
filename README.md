# Serverless Scheduler

AWS based serverless solution for scheduling and running tasks.
The main use at the moment is monitoring websites for changes in HTML, however it's easy to extend it with plugins that can be implemented to do whatever you like.

If your workflow fits the generic "every `n` minutes do `something`" and you're willing to implement a plugin for `something` then it can be done with this project.

The API and scheduler core are pretty stable as of now, but the frontend still requires a major refactor (to properly get supported job types that were added as a plugin).

For a similar thing but hardcoded to just HTTP monitoring jobs and deployable in Kubernetes cluster look at [old monitor-page repo](https://github.com/dezeroku/monitor-page).

In reality if you don't need it to scale to the moon your best bet is to use a widely recognized project such as [changedetection.io](https://github.com/dgtlmoon/changedetection.io).
Don't use this in production :D

# Architecture

![Architecture](docs/diagrams/created/high_level_overview.png?raw=true "High Level Overview")

[Read more about architecture](docs/md/architecture.md).

# How to deploy it?

## TL;DR

Prepare your own `*-secret-values.tfvars` files based on `.example` files in `config/<DEPLOY_ENV>/`, and run

```
./utils/complete_build.sh
./utils/complete_deploy.sh
```

## Further reading

[Deploying a single part of the system](docs/md/deployments.md).
[Plugins](docs/md/plugins.md).

# How does it look?

Couple screenshots from the provided web UI.

![Home Page (empty)](docs/static/front/home.png?raw=true "Home Page (empty)")
![Task Creation](docs/static/front/create.png?raw=true "Task Creation")
![Home Page](docs/static/front/added.png?raw=true "Home Page")
![Modify Modal](docs/static/front/modify.png?raw=true "Modify Modal")
