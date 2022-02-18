import json
import logging
import os

from lambda_decorators import cors_headers

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@cors_headers
def login(event, context):
    try:
        # TODO: the scope list could be generated in serverless based on the CF
        location = "https://" + \
        "auth." + \
        os.getenv('FRONT_DOMAIN') + \
        "/oauth2/authorize?client_id=" + \
        os.getenv('CLIENT_POOL_ID') + \
        "&response_type=token&scope=" + \
        "aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=" + \
        "https://" + os.getenv('FRONT_DOMAIN') + \
        "/login/cognito-parser"
    except Exception as e:
        logger.exception(e)

    response = {}
    response["statusCode"]=302
    response["headers"]={'Location': location}
    data = {}
    response["body"]=json.dumps(data)
    return response

@cors_headers
def logout(event, context):
    try:
        location = "https://" + \
        "auth." + \
        os.getenv('FRONT_DOMAIN') + \
        "/logout?client_id=" + \
        os.getenv('CLIENT_POOL_ID') + \
        "&logout_uri=" + \
        "https://" + os.getenv('FRONT_DOMAIN') + "/logout"
    except Exception as e:
        logger.exception(e)

    response = {}
    response["statusCode"]=302
    response["headers"]={'Location': location}
    data = {}
    response["body"]=json.dumps(data)
    return response
