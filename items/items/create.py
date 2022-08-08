import logging

from lambda_decorators import cors_headers, json_schema_validator, load_json_body

from common import cognito, utils
from common.json_schemas import item_schema, itemwithid_schema
from items.schemas import MonitorJobSchema, UserDataSchema

logger = logging.getLogger()
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
    return MonitorJobSchema().load(body)


# TODO: get through these decorators properly, they don't seem to run from the bottom-up?
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
    table = utils.get_dynamo_table()
    user = cognito.get_username(event)
    payload = event["body"]

    return handler(table, user, payload)


def handler(table, user, payload):
    # Extend the current data assigned to a user
    # with new monitor entry
    db_data = table.get_item(Key={"id": user})["Item"]
    user_data = UserDataSchema().load(db_data)

    # Doing it this way is rather ugly...
    # TODO: There is a risk of conflicting IDs in case too many requests for
    # the same user come at the same time.
    # Not a big change for that, but it WILL be annoying
    next_id = generate_next_id(user_data)
    to_add = get_monitor_job_with_id(payload, next_id)
    to_add_json = MonitorJobSchema().dump(to_add)
    logger.info(to_add_json)

    result = table.update_item(
        Key={"id": user},
        UpdateExpression="SET monitors = list_append(monitors, :i)",
        ExpressionAttributeValues={
            ":i": [to_add_json],
        },
        ReturnValues="UPDATED_NEW",
    )

    status_code = result["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        body = utils.replace_decimals(to_add_json)
    else:
        body = {}

    return {"statusCode": status_code, "body": body}
