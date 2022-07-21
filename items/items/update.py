import logging

from lambda_decorators import (
    cors_headers,
    json_http_resp,
    json_schema_validator,
    load_json_body,
)

from common import cognito, utils
from common.schemas import item_schema

from items.schemas import UserDataSchema, MonitorJobSchema

logger = logging.getLogger()
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
    table = utils.get_dynamo_table()

    user = cognito.get_username(event)

    item_id = int(event["pathParameters"]["item_id"])

    result = table.get_item(Key={"id": user})["Item"]
    schema = UserDataSchema()
    user_data = schema.load(result)

    to_update = event["body"]
    to_update["id"] = item_id

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

    response = table.put_item(Item=to_save)

    return {"statusCode": 200}
