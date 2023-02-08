## Items

This subproject defines few lambdas that are available for an authorized user
and provide REST API responsible for:

1. items.get.get -> listing existing monitoring jobs
2. items.create.create -> creating new monitoring jobs
3. items.delete.delete -> deleting monitoring jobs
4. items.update -> modifying existing monitoring jobs

Lambdas assume that:

1. Events come in with authorization data from api-gateway (JWT)
2. User's initial data is already inserted in the table

Data is persisted in DynamoDB. Name of the table should be passed via env as `DYNAMO_DB` variable.

## Development

Each function's entry point is responsible for getting the required params and passing these to
actual handler functions (which are UT covered).
Entry points themselves are not covered as of now.

To set up local env, install dependencies and trigger the UTs run the following snippet:

```
poetry env use python3.8
poetry install
poetry run pytest
```

### TODOs

1. items.get.get sets up initial user data (entry with no monitors defined) if it's not found in the table.
   This should be rewritten, so the initial data is inserted outside of this module (preferably when user is registered to Cognito, appropriate Lambda function should be triggered).
   This currently breaks assumption 2.
