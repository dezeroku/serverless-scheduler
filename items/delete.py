import logging

from lambda_decorators import cors_headers

from common import cognito
from common import utils

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@cors_headers
def delete(event, context):
    table = utils.get_dynamo_table()

    user = cognito.get_username(event)

    item_id = int(event['pathParameters']['item_id'])

    result = table.get_item(
        Key={
            'user_id': user
        }
    )['Item']

    result['monitors'] = list(filter(lambda x: x['id'] != item_id, result['monitors']))

    response = table.put_item(Item=result)

    return {'statusCode': 200}
