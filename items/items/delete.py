import logging

import botocore.exceptions
from lambda_decorators import cors_headers

from common import cognito, utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cors_headers
def delete(event, context):
    # pylint: disable=unused-argument
    table = utils.get_dynamo_table()
    user = cognito.get_username(event)
    item_id = int(event["pathParameters"]["item_id"])

    return handler(table, user, item_id)


def handler(table, user, item_id):
    # Delete entry (assigned to user), identified by item_id, from DB

    # ConditionExpression is a dummy way to check if deletion happened or not
    # TODO: is it really cheaper (less operations) than checking via read?
    # Do we even need to do it?
    try:
        table.delete_item(
            Key={"user_id": user, "job_id": item_id},
            ConditionExpression="(attribute_exists(user_id))",
        )
    except botocore.exceptions.ClientError as exc:
        # duplicated code with update
        # pylint: disable=R0801
        # TODO: this just looks... wrong
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {"statusCode": 404}

        logger.debug(exc)
        return {"statusCode": 500}

    return {"statusCode": 200}
