## Items

This subproject defines few lambdas that are available for an authorized user
and provide REST API responsible for:

1. items.get.get -> listing existing monitoring jobs
2. items.create.create -> creating new monitoring jobs
3. items.delete.delete -> deleting monitoring jobs
4. items.update -> modifying existing monitoring jobs

Lambdas assume that:

1. Events come in with authorization data from api-gateway (JWT)

Data is persisted in DynamoDB. Name of the table should be passed via env as `DYNAMO_DB` variable.

Additionaly, the `items.schedule_queue.add` function is responsible for reading DynamoDB stream changes
and converting these to `SchedulerChangeEvent` objects, which are put to SQS queue and consumed further
down the line by another microservice.

## Development

Each function's entrypoint is responsible for getting the required params and passing these to
actual handler functions (which are fully UT covered).
The entrypoints themselves also are covered in most cases, but not as thoroughly.

To set up local env, install dependencies and trigger the UTs run the following snippet:

```
poetry env use python3.9
poetry install
poetry run pytest
```
