import logging

import botocore
from lambda_decorators import cors_headers, json_schema_validator, load_json_body

from common import cognito, utils
from common.json_schemas import item_schema
from items.models import MonitorJob

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
    user_email = cognito.get_email(event)
    table = utils.get_dynamo_table()
    item_id = int(event["pathParameters"]["item_id"])
    payload = event["body"]

    return handler(table, user_email, item_id, payload)


def handler(table, user_email, item_id, payload):
    # Update the item kept under `item_id` with
    # data that was sent in the request
    to_update = payload
    to_update["job_id"] = item_id
    to_update["user_email"] = user_email
    to_update_dict = MonitorJob(**to_update).dict()

    try:
        table.put_item(
            Item=to_update_dict,
            ConditionExpression="(attribute_exists(user_email))",
        )
    except botocore.exceptions.ClientError as exc:
        # duplicated code with delete
        # pylint: disable=R0801
        # TODO: this just looks... wrong
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {"statusCode": 404}

        logger.debug(exc)
        return {"statusCode": 500}

    return {"statusCode": 200}
