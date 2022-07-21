import logging

from lambda_decorators import (
    cors_headers,
    json_http_resp,
    json_schema_validator,
    load_json_body,
)

from common import cognito, utils
from common.common_schemas import item_schema, itemwithid_schema

from items.schemas import UserDataSchema, MonitorJobSchema

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
@json_http_resp
@load_json_body
@json_schema_validator(
    request_schema={
        "type": "object",
        "properties": {"body": item_schema},
    },
    response_schema=itemwithid_schema,
)
def create(event, context):
    table = utils.get_dynamo_table()

    user = cognito.get_username(event)

    return handler(user, table, event["body"])


def handler(user, table, payload):
    # Extend the current data assigned to a user
    # with new monitor entry
    db_data = table.get_item(Key={"id": user})["Item"]
    user_data = UserDataSchema().load(db_data)

    next_id = generate_next_id(user_data)
    to_add = get_monitor_job_with_id(payload, next_id)
    user_data.monitors.append(to_add)

    logger.info(user_data)

    to_save = UserDataSchema().dump(user_data)
    response = table.put_item(Item=to_save)

    to_return = dict(MonitorJobSchema().dump(to_add))
    return utils.replace_decimals(to_return)
