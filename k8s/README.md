# Kubernetes manifests

By default monitor-page namespace is used.
Currently there is one user limit for deployment (just naming stuff).

Two secrets have to be manually provided:
* `secret-registry` that contains `dockerconfigjson` data required to access private Docker registry.
* `secret-sendgrid` that provided `api-key` entry containing, well... API key to sendgrid (it's used by mail senders)
