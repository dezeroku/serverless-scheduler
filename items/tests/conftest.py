import copy

import boto3
import pytest
from moto import mock_dynamodb

from items.models import MonitorJob, UserData
from items.schemas import MonitorJobSchema, UserDataSchema


@pytest.fixture
def example_user_data(
    example_monitor_job,
):
    temp = UserDataSchema().load(Helpers().UserDataJSONFactory(id="example_user"))
    temp.monitors.append(example_monitor_job)

    return temp


@pytest.fixture
def example_empty_user_data():
    return UserDataSchema().load(Helpers().UserDataJSONFactory(id="example_user"))


@pytest.fixture
def example_monitor_job():
    return MonitorJobSchema().load(Helpers().MonitorJobJSONFactory())


@pytest.fixture
def example_empty_user_data_json():
    return Helpers().UserDataJSONFactory(id="example_user")


@pytest.fixture
def example_monitor_job_json():
    return Helpers().MonitorJobJSONFactory()


class Helpers:
    @staticmethod
    def UserDataJSONFactory(
        *,
        id,
        monitors=[],
    ):
        return {
            "id": id,
            "monitors": monitors,
        }

    @staticmethod
    def MonitorJobJSONFactory(
        *,
        id=1,
        make_screenshots=True,
        sleep_time=1,
        url="http://example.com",
    ):
        return {
            "id": id,
            "makeScreenshots": make_screenshots,
            "sleepTime": sleep_time,
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

            temp = {"jwt": {"claims": {"username": cognitoUsername}}}
            # https://stackoverflow.com/a/11416002 :)
            # Modifying requestContext indirectly here, causes the change to be
            # "remembered"
            event["requestContext"] = copy.deepcopy(event["requestContext"])
            event["requestContext"]["authorizer"] = temp

        return event

    @staticmethod
    def empty_mock_table(dynamodb, table_name):
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        return table

    @staticmethod
    def insert_mock_user(table, user):
        # Set up dummy user
        user_data = UserDataSchema().load({"id": user})
        to_save = UserDataSchema().dump(user_data)
        table.put_item(Item=to_save)


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
        dynamodb = boto3.resource("dynamodb")

        table = Helpers.empty_mock_table(dynamodb, table_name)

        yield table


@pytest.fixture
def mock_db(db_user, table_name):
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb")

        table = Helpers.empty_mock_table(dynamodb, table_name)

        Helpers.insert_mock_user(table, db_user)

        yield dynamodb
