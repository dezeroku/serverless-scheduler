import logging

from lambda_decorators import (
    cors_headers,
    json_http_resp,
    json_schema_validator,
    load_json_body,
)

from common import cognito
from common import utils
from common.schemas import item_schema

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@cors_headers
@load_json_body
@json_schema_validator(
    request_schema={"type": "object", "properties": {"body": item_schema}}
)
def update(event, context):
    table = utils.get_dynamo_table()

    user = cognito.get_username(event)

    item_id = int(event["pathParameters"]["item_id"])

    result = table.get_item(Key={"id": user})["Item"]

    to_update = event["body"]
    to_update["id"] = item_id

    result["monitors"] = list(
        map(lambda x: x if x["id"] != item_id else to_update, result["monitors"])
    )

    logger.info(result)

    response = table.put_item(Item=result)

    return {"statusCode": 200}
