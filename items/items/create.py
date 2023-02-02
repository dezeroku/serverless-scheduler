import logging

from lambda_decorators import cors_headers, json_schema_validator, load_json_body

from common import cognito, utils
from common.json_schemas import item_schema, itemwithid_schema
from items.models import MonitorJob, UserData

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def generate_next_id(user_data):
    # Get the current highest id and add 1 to it
    return (
        max(
            list(
                map(
                    lambda x: x.id,
                    user_data.monitors,
                )
            )
            + [0]
        )
        + 1
    )


def get_monitor_job_with_id(body, next_id):
    body["id"] = next_id
    return MonitorJob(**body)


@cors_headers
@load_json_body
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

    return handler(table, user, payload)


def handler(table, user, payload):
    # Extend the current data assigned to a user
    # with new monitor entry
    db_data = table.get_item(Key={"id": user})["Item"]
    user_data = UserData(**db_data)

    # Doing it this way is rather ugly...
    # There is a risk of conflicting IDs in case too many requests for
    # the same user come at the same time.
    # Not a big change for that, but it WILL be annoying
    next_id = generate_next_id(user_data)
    to_add = get_monitor_job_with_id(payload, next_id)
    to_add_json = to_add.dict()
    logger.info(to_add_json)

    result = table.update_item(
        Key={"id": user},
        UpdateExpression="SET monitors = list_append(monitors, :i)",
        ExpressionAttributeValues={
            ":i": [to_add_json],
        },
        ReturnValues="UPDATED_NEW",
    )

    if (status_code := result["ResponseMetadata"]["HTTPStatusCode"]) == 200:
        body = utils.replace_decimals(to_add_json)
    else:
        body = {}

    return {"statusCode": status_code, "body": body}
