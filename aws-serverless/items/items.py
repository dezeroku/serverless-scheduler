import json
import logging
import os

from lambda_decorators import cors_headers, json_http_resp
import boto3
dynamodb = boto3.resource('dynamodb')

from common import cognito

# To be used later on with schemas
from common.schemas import itemwithid_schema

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@cors_headers
@json_http_resp
def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMO_DB'])

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

    return result['Item']['monitors']
