import logging

import botocore.exceptions
from lambda_decorators import cors_headers

from items import cognito, utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cors_headers
def delete(event, context):
    # pylint: disable=unused-argument
    table = utils.get_dynamo_table()
    user_id = cognito.get_username(event)
    job_id = int(event["pathParameters"]["job_id"])

    return handler(table, user_id, job_id)


def handler(table, user_id, job_id):
    # Delete entry (assigned to user), identified by job_id, from DB

    # ConditionExpression is a dummy way to check if deletion happened or not
    # TODO: is it really cheaper (less operations) than checking via read?
    # Do we even need to do it?
    try:
        table.delete_item(
            Key={"user_id": user_id, "job_id": job_id},
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
