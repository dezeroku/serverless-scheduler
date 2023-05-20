# Deployments

## Deployment of a singular component

Each group has its own terraform "blocks", that define parts of the infra.
The are multiple blocks per group, as terraform handles both the core infra (e.g. `items-infra`), but also code deployments (e.g. `items-front-upload`).

Situation is a bit complicated at the moment, but for `items`:

1. There is terraform module for deploying core infra (needs to be run on init)
2. There is terraform module for uploading front files (needs to be run when front changes)
3. There is a terraform module for deploying lambdas and attaching them to API Gateway (needs to be run when backend changes)

First build the packages by issuing

```
./utils/build.sh items
```

then prepare the `config/<DEPLOY_ENV>/items-infra-secret-values.tfvars` (you can base on `config/<DEPLOY_ENV>/items-infra-secret-values.tfvars.example` and finally

```
DEPLOY_ENV=<ENV> ./utils/deploy.sh items-infra
DEPLOY_ENV=<ENV> ./utils/deploy.sh items-front-upload
DEPLOY_ENV=<ENV> ./utils/deploy.sh items-lambdas-upload
```
