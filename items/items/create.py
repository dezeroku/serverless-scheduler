import logging

from boto3.dynamodb.conditions import Key
from lambda_decorators import (
    cors_headers,
    json_http_resp,
    json_schema_validator,
    load_json_body,
)

from common import cognito, utils
from common.json_schemas import item_schema, itemwithid_schema
from items.models import MonitorJob

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_monitor_job_with_id(body, next_id):
    body["job_id"] = next_id
    return MonitorJob(**body)


@cors_headers
@load_json_body
@json_http_resp
@json_schema_validator(
    request_schema={
        "type": "object",
        "properties": {"body": item_schema},
    },
    response_schema={
        "type": "object",
        "properties": {"body": itemwithid_schema},
    },
)
def create(event, context):
    # pylint: disable=unused-argument
    table = utils.get_dynamo_table()
    user = cognito.get_username(event)
    payload = event["body"]
    payload["user_id"] = user

    response = handler(table, user, payload)
    # TODO: is the output here correct or should I jsonify it?
    # response["body"] = json.dumps(response["body"])
    return response


def handler(table, user, payload):
    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user), ScanIndexForward=False, Limit=1
    )

    if not (last_monitor_job_result := response["Items"]):
        logger.debug("First entry for user")
        next_id = 0
    else:
        # Doing it this way is rather ugly...
        # There is a risk of conflicting IDs in case too many requests for
        # the same user come at the same time.
        # Not a big change for that, but it WILL be annoying
        # probably better to use UUIDs or check for conflicts at the creation time?
        next_id = MonitorJob(**last_monitor_job_result.pop()).job_id + 1

    to_add = get_monitor_job_with_id(payload, next_id)
    to_add_dict = to_add.dict()
    logger.info(to_add_dict)

    result = table.put_item(Item=to_add_dict)

    logger.debug(result)

    if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
        body = to_add.dict()
    else:
        body = {}

    return body
