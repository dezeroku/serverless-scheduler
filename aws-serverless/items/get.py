import logging

from lambda_decorators import cors_headers, json_http_resp, json_schema_validator

from common import cognito
from common import utils
from common.schemas import itemwithid_schema

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@cors_headers
@json_http_resp
@json_schema_validator(response_schema={'type': 'array', 'items': itemwithid_schema})
def get(event, context):
    table = utils.get_dynamo_table()

    user = cognito.get_username(event)

    # Actually getting the data from a row:
    result = table.get_item(
        Key={
            'user_id': user
        }
    )


    # TODO: This is a big hack
    # such a logic should be handled on the Lambda level
    # This Lambda should listed to signup events of the cognito pool
    # and create rows as needed accordingly
    # Row creation if needed
    if 'Item' not in result:
        logger.info(f'HACK: putting the initial data for {user} in the table')
        response = table.put_item(
        Item={
                'user_id': user,
                'monitors': []
            }
        )

        # Doing it in such an ugly way, to make sure that the data is in place
        result = table.get_item(
            Key={
                'user_id': user
            }
        )

    return utils.replace_decimals(result['Item']['monitors'])
