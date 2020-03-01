# Kubernetes manifests

TODO: properly handle RBAC permissions
TODO: some bad stuff happens when you do many operations that work on same deployment in a short time, seems to be under control with normal usage

By default monitor-page namespace is used.
Currently there is one user limit for deployment (just naming stuff).
Postgres DB is set up in the cluster already, and it's not described in these manifests.

These secrets have to be manually provided:
* `secret-registry` that contains `dockerconfigjson` data required to access private Docker registry.
* `secret-sendgrid` that provides `api-key` entry containing, well... API key to sendgrid (it's used by mail senders)
* `secret-jwt`      that provides `jwt-secret` entry containing value that's a base for JWT
