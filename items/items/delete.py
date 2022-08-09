import logging

from lambda_decorators import cors_headers

from common import cognito, utils
from items.schemas import MonitorJobSchema, UserDataSchema

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@cors_headers
def delete(event, context):
    table = utils.get_dynamo_table()
    user = cognito.get_username(event)
    item_id = int(event["pathParameters"]["item_id"])

    return handler(table, user, item_id)


def handler(table, user, item_id):
    # Delete entry (assigned to user), identified by item_id, from DB

    result = table.get_item(Key={"id": user})["Item"]
    schema = UserDataSchema()
    user_data = schema.load(result)

    length = len(user_data.monitors)
    index = [x for x in range(0, length) if user_data.monitors[x].id == item_id]

    if not index:
        logger.debug("Entry not found for id: %s", item_id)
        return {"statusCode": 404}
    else:
        index = index[0]

    query = "REMOVE monitors[%d]" % (index)
    table.update_item(Key={"id": user}, UpdateExpression=query)

    return {"statusCode": 200}
