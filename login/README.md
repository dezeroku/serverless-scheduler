## login

This subproject defines two helpers:
1. login
2. logout

These are responsible for providing a static API endpoint (e.g. /login) on API-Gateway level and then redirect to proper cognito URL. The work that is done here should most likely be handled somewhere else, e.g. after the resources are created in AWS, front module should be rebuilt and proper URLs hardcoded on its level.
