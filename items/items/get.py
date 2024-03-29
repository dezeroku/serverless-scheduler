import logging

from boto3.dynamodb.conditions import Key

from common.models.jobs import ScheduledJob
from items import cognito, utils
from items.json_schemas import jobwithid_schema
from items.libs.lambda_decorators import (
    cors_headers,
    json_http_resp,
    json_schema_validator,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cors_headers
@json_http_resp
@json_schema_validator(
    response_schema={
        "type": "array",
        "items": jobwithid_schema,
    }
)
def get(event, context):
    # pylint: disable=unused-argument
    table = utils.get_dynamo_table()
    user_id = cognito.get_username(event)

    return handler(table, user_id)


def handler(table, user_id, pagination=True):
    # Return the data kept in DB for user ID
    # By default returns ALL the results, taking pagination into account
    response = table.query(KeyConditionExpression=Key("user_id").eq(user_id))

    monitor_jobs: list[ScheduledJob] = response["Items"]

    if pagination:
        while "LastEvaluatedKey" in response:
            response = table.query(
                KeyConditionExpression=Key("user_id").eq(user_id),
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            monitor_jobs.extend(response["Items"])

    return utils.replace_decimals(monitor_jobs)
