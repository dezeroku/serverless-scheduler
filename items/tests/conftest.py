import copy

import boto3
import mypy_boto3_dynamodb
import pytest
from moto import mock_dynamodb

from items.models import MonitorJob


@pytest.fixture
def example_monitor_job():
    return MonitorJob(**Helpers().MonitorJobJSONFactory())


@pytest.fixture
def example_monitor_job_json():
    return Helpers().MonitorJobJSONFactory()


class Helpers:
    @staticmethod
    def MonitorJobJSONFactory(
        *,
        user_id="example_user",
        job_id=1,
        make_screenshots=True,
        sleep_time=1,
        url="http://example.com",
    ):
        return {
            "user_id": user_id,
            "job_id": job_id,
            "make_screenshots": make_screenshots,
            "sleep_time": sleep_time,
            "url": url,
        }

    @staticmethod
    def EventFactory(
        resource="/",
        path="/",
        httpMethod="GET",
        requestContext={
            "resourcePath": "/",
            "httpMethod": "GET",
            "path": "/",
        },
        headers={},
        multiValueHeaders={},
        queryStringParameters=None,
        multiValueQueryStringParameters=None,
        pathParameters=None,
        stageVariables=None,
        body=None,
        isBase64Encoded=False,
        cognitoUsername=None,
    ):
        assert httpMethod == requestContext.get("httpMethod")

        event = {
            "resource": resource,
            "path": path,
            "httpMethod": httpMethod,
            "requestContext": requestContext,
            "headers": headers,
            "multiValueHeaders": multiValueHeaders,
            "queryStringParameters": queryStringParameters,
            "multiValueQueryStringParameters": multiValueQueryStringParameters,
            "pathParameters": pathParameters,
            "stageVariables": stageVariables,
            "body": body,
            "isBase64Encoded": isBase64Encoded,
        }

        if cognitoUsername:
            if event.get("requestContext").get("authorizer", None):
                raise ValueError(
                    "cognitoUsername passed together with requestContext.authorizer"
                )

            temp = {"jwt": {"claims": {"email": cognitoUsername}}}
            # https://stackoverflow.com/a/11416002 :)
            # Modifying requestContext indirectly here, causes the change to be
            # "remembered"
            event["requestContext"] = copy.deepcopy(event["requestContext"])
            event["requestContext"]["authorizer"] = temp

        return event

    @staticmethod
    def empty_mock_table(dynamodb: mypy_boto3_dynamodb.ServiceResource, table_name):
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "job_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "job_id", "AttributeType": "N"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        return table


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture
def example_event():
    return {
        "resource": "/",
        "path": "/",
        "httpMethod": "GET",
        "requestContext": {
            "resourcePath": "/",
            "httpMethod": "GET",
            "path": "/Prod/",
        },
        "headers": {"header": "header-value"},
        "multiValueHeaders": {},
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "body": None,
        "isBase64Encoded": False,
    }


@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os

    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture()
def db_user():
    return "example_user"


@pytest.fixture()
def table_name():
    return "items_ut"


@pytest.fixture
def empty_mock_db(table_name):
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb")

        table = Helpers.empty_mock_table(dynamodb, table_name)

        yield dynamodb


@pytest.fixture
def mock_db_table(table_name):
    with mock_dynamodb():
        dynamodb: mypy_boto3_dynamodb.ServiceResource = boto3.resource("dynamodb")

        table = Helpers.empty_mock_table(dynamodb, table_name)

        yield table


@pytest.fixture
def mock_db(db_user, table_name):
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb")

        table = Helpers.empty_mock_table(dynamodb, table_name)

        yield dynamodb
