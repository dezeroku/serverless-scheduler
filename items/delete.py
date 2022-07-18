import logging

from lambda_decorators import cors_headers
from common import cognito, utils
from schemas import UserDataSchema, MonitorJobSchema

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@cors_headers
def delete(event, context):
    table = utils.get_dynamo_table()

    user = cognito.get_username(event)

    item_id = int(event["pathParameters"]["item_id"])

    result = table.get_item(Key={"id": user})["Item"]
    schema = UserDataSchema()
    user_data = schema.load(result)

    user_data.monitors = list(
        filter(
            lambda x: x.id != item_id,
            user_data.monitors,
        )
    )

    to_save = schema.dump(user_data)
    response = table.put_item(Item=to_save)

    return {"statusCode": 200}
