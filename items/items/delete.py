import logging

from lambda_decorators import cors_headers

from common import cognito, utils
from items.models import UserData

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

    result = table.get_item(Key={"id": user})["Item"]
    user_data = UserData(**result)

    length = len(user_data.monitors)

    if not (
        index := [x for x in range(0, length) if user_data.monitors[x].id == item_id]
    ):
        logger.debug("Entry not found for id: %s", item_id)
        return {"statusCode": 404}

    index = index[0]

    query = f"REMOVE monitors[{index}]"

    # Need to handle errors?
    table.update_item(Key={"id": user}, UpdateExpression=query)

    return {"statusCode": 200}
