import json
import logging
import os

from lambda_decorators import cors_headers
import boto3
dynamodb = boto3.resource('dynamodb')

from common import cognito

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@cors_headers
def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMO_DB'])

    user = cognito.get_username(event)


    # Actually getting the data from a row:

    result = table.get_item(
        Key={
            'user_id': user
        }
    )

    if 'Item' not in result:
        # TODO: This is a big hack
        # such a logic should be handled on the Lambda level
        # This Lambda should listed to signup events of the cognito pool
        # and create rows as needed accordingly
        # Row creation if needed

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

    logger.info(result)

    status_code = 200
    content = result['Item']['monitors']

    return {'statusCode': status_code, 'body': json.dumps(content)}
