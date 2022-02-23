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

    result = table.get_item(
        Key={
            'user_id': user
        }
    )

    logger.info(result)

    status_code = 200
    content = result['Item']['monitors']

    return {'statusCode': status_code, 'body': json.dumps(content)}
