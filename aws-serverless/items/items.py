import json
import logging
import os

from common import cognito

from lambda_decorators import cors_headers

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@cors_headers
def get(event, context):
    status_code = 200
    content = []

    logger.info(cognito.get_username(event))
    # Return the data from DynamoDB

    return {'statusCode': status_code, 'body': json.dumps(content)}
