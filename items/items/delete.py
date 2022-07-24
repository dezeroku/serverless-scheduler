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
    # Delete entry (assigned to user) identified by item_id from DB

    result = table.get_item(Key={"id": user})["Item"]
    schema = UserDataSchema()
    user_data = schema.load(result)

    len_before = len(user_data.monitors)

    user_data.monitors = list(
        filter(
            lambda x: x.id != item_id,
            user_data.monitors,
        )
    )

    len_after = len(user_data.monitors)

    if len_before == len_after:
        logger.debug("Entry not found for id: %s", item_id)
        return {"statusCode": 404}

    to_save = schema.dump(user_data)
    response = table.put_item(Item=to_save)

    return {"statusCode": 200}
