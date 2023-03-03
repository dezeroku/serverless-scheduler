import logging

import botocore

from common.models.plugins import parse_dict_to_job
from items import cognito, utils
from items.json_schemas import job_schema
from items.libs.lambda_decorators import (
    cors_headers,
    json_schema_validator,
    load_json_body,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cors_headers
@load_json_body
@json_schema_validator(
    request_schema={
        "type": "object",
        "properties": {"body": job_schema},
    }
)
def update(event, context):
    # pylint: disable=unused-argument
    user_email = cognito.get_email(event)
    user_id = cognito.get_username(event)
    table = utils.get_dynamo_table()
    job_id = int(event["pathParameters"]["job_id"])
    payload = event["body"]

    return handler(table, user_email, user_id, job_id, payload)


def handler(table, user_email, user_id, job_id, payload):
    # Update the item kept under `job_id` with
    # data that was sent in the request
    to_update = payload
    to_update["job_id"] = job_id
    to_update["user_email"] = user_email
    to_update["user_id"] = user_id
    to_update_dict = parse_dict_to_job(to_update).dict()

    try:
        table.put_item(
            Item=to_update_dict,
            ConditionExpression="(attribute_exists(user_id))",
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
