import logging

from lambda_decorators import cors_headers, json_schema_validator, load_json_body

from common import cognito, utils
from common.json_schemas import item_schema
from items.schemas import MonitorJobSchema, UserDataSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cors_headers
@load_json_body
@json_schema_validator(
    request_schema={
        "type": "object",
        "properties": {"body": item_schema},
    }
)
def update(event, context):
    # pylint: disable=unused-argument
    user = cognito.get_username(event)
    table = utils.get_dynamo_table()
    item_id = int(event["pathParameters"]["item_id"])
    payload = event["body"]

    return handler(table, user, item_id, payload)


def handler(table, user, item_id, payload):
    # Update the item kept under `item_id` with
    # data that was sent in the request
    result = table.get_item(Key={"id": user})["Item"]
    schema = UserDataSchema()
    user_data = schema.load(result)

    to_update = payload
    to_update["id"] = item_id

    # Check if the item to update actually exists
    if not any(filter(lambda x: x.id == item_id, user_data.monitors)):
        return {"statusCode": 404}

    schema = MonitorJobSchema()
    to_update = schema.load(to_update)

    user_data.monitors = list(
        map(
            lambda x: x if x.id != item_id else to_update,
            user_data.monitors,
        )
    )

    logger.info(user_data)

    to_save = UserDataSchema().dump(user_data)

    table.put_item(Item=to_save)

    return {"statusCode": 200}
