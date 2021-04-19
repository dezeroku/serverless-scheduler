# monitor_page

Bunch of containers to manage checking websites for changes.
Allows to send emails (optionally with rendered images showing differences) and easily manage everything from the UI level.
Contains all necessary manifests to deploy on Kubernetes in `monitor-page` namespace.

## Structure
* screenshot making container - screenshoter, API, internal service
* picture comparing container - comparator, API, internal service
* html checking container - checker, no service here (that's common worker here)
* sender - sender, sends mesage with data it gets using one of (mail, SMS (TODO), messenger(TODO)) , internal service
* manager container - manager, manages pods that actually do the checking job, reads/writes db, API container, service
* frontend container - frontend, allows user to login based on supported emails and one-time passwords, contacts API, reads DB
* db container - postgres, handled with postgres-operator on k8s

### TODOs
* Switch k8s manifests to helm for easier configuration
* Write tests
