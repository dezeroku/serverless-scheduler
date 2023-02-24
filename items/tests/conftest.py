import copy
import os

import boto3
import mypy_boto3_dynamodb
import mypy_boto3_sqs
import pytest
from boto3.dynamodb.conditions import Key
from moto import mock_dynamodb, mock_sqs

_EXAMPLE_USER_EMAIL = "user@example.com"
_EXAMPLE_QUEUE_NAME = "test.fifo"


class Helpers:
    @staticmethod
    def html_monitor_job_dict_factory(
        *,
        user_email=_EXAMPLE_USER_EMAIL,
        job_id=1,
        make_screenshots=True,
        sleep_time=1,
        url="http://example.com",
    ):
        return {
            "user_email": user_email,
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
        requestContext=None,
        queryStringParameters=None,
        multiValueQueryStringParameters=None,
        pathParameters=None,
        body=None,
        cognitoEmail=None,
    ):
        # pylint: disable=invalid-name,too-many-arguments

        if requestContext is None:
            requestContext = {
                "resourcePath": "/",
                "httpMethod": "GET",
                "path": "/",
            }

        assert httpMethod == requestContext.get("httpMethod")

        event = {
            "resource": resource,
            "path": path,
            "httpMethod": httpMethod,
            "requestContext": requestContext,
            "queryStringParameters": queryStringParameters,
            "multiValueQueryStringParameters": multiValueQueryStringParameters,
            "pathParameters": pathParameters,
            "body": body,
        }

        if cognitoEmail:
            if event.get("requestContext").get("authorizer", None):
                raise ValueError(
                    "cognitoEmail passed together with requestContext.authorizer"
                )

            temp = {"jwt": {"claims": {"email": cognitoEmail}}}
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
                {"AttributeName": "user_email", "KeyType": "HASH"},
                {"AttributeName": "job_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_email", "AttributeType": "S"},
                {"AttributeName": "job_id", "AttributeType": "N"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        return table

    @staticmethod
    def empty_mock_sqs(sqs: mypy_boto3_sqs.SQSClient, queue_name):
        sqs.create_queue(
            QueueName=queue_name,
            Attributes={"FifoQueue": "true", "ContentBasedDeduplication": "true"},
        )

    @staticmethod
    def get_monitor_jobs_for_user(table, user_email):
        return table.query(KeyConditionExpression=Key("user_email").eq(user_email))[
            "Items"
        ]


@pytest.fixture(name="helpers")
def helpers_fixture():
    return Helpers


@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(name="db_user")
def db_user_fixture():
    return _EXAMPLE_USER_EMAIL


@pytest.fixture(name="table_name")
def table_name_fixture():
    return "items_ut"


@pytest.fixture
def empty_mock_db(table_name):
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb")

        Helpers.empty_mock_table(dynamodb, table_name)

        yield dynamodb


@pytest.fixture
def mock_db_table(table_name):
    with mock_dynamodb():
        dynamodb: mypy_boto3_dynamodb.ServiceResource = boto3.resource("dynamodb")

        table = Helpers.empty_mock_table(dynamodb, table_name)

        yield table


@pytest.fixture
def mock_db(table_name):
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb")

        Helpers.empty_mock_table(dynamodb, table_name)

        yield dynamodb


@pytest.fixture(name="example_queue_name")
def example_queue_name_fixture():
    return _EXAMPLE_QUEUE_NAME


@pytest.fixture(name="mock_sqs")
def mock_sqs_fixture(example_queue_name):
    with mock_sqs():
        sqs = boto3.client("sqs")

        Helpers.empty_mock_sqs(sqs, example_queue_name)

        yield sqs
