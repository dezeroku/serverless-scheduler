import logging

from lambda_decorators import cors_headers, json_http_resp, json_schema_validator

from common import cognito, utils
from common.json_schemas import itemwithid_schema
from items.models import UserData

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cors_headers
@json_http_resp
@json_schema_validator(
    response_schema={
        "type": "array",
        "items": itemwithid_schema,
    }
)
def get(event, context):
    # pylint: disable=unused-argument
    table = utils.get_dynamo_table()
    user = cognito.get_username(event)

    return handler(table, user)


def handler(table, user):
    # Return the data kept in DB unser user ID

    # Actually getting the data from a row:
    result = table.get_item(Key={"id": user})

    # This is a big hack
    # such a logic should be handled on the Lambda level
    # This Lambda should listen to signup events of the cognito pool
    # and create rows as needed accordingly
    # The case should be probably similar for user removal, but it's not as
    # important for now
    # Row creation if needed
    if "Item" not in result:
        logger.info("HACK: putting the initial data for %s in the table", user)

        user_data = UserData(id=user)
        to_save = user_data.dict()
        table.put_item(Item=to_save)

        # Doing it in such an ugly way, to make sure that the data is in place
        result = table.get_item(Key={"id": user})
        user_data = UserData(**result["Item"])
    else:
        user_data = UserData(**result["Item"])

    to_return = user_data.dict()
    return utils.replace_decimals(to_return["monitors"])
