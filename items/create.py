import logging

from lambda_decorators import (
    cors_headers,
    json_http_resp,
    json_schema_validator,
    load_json_body,
)

from common import cognito
from common import utils
from common.schemas import item_schema, itemwithid_schema

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# TODO: get through these decorators properly, they don't seem to run from the bottom-up?
@cors_headers
@json_http_resp
@load_json_body
@json_schema_validator(
    request_schema={"type": "object", "properties": {"body": item_schema}},
    response_schema=itemwithid_schema,
)
def create(event, context):
    table = utils.get_dynamo_table()

    user = cognito.get_username(event)

    result = table.get_item(Key={"user_id": user})["Item"]

    # Generating the next id
    next_id = max(list(map(lambda x: x["id"], result["monitors"])) + [0]) + 1

    to_add = event["body"]
    to_add["id"] = next_id

    result["monitors"] = result["monitors"] + [to_add]

    logger.info(result)

    response = table.put_item(Item=result)

    return utils.replace_decimals(to_add)
