import os
from decimal import Decimal

import boto3
from mypy_boto3_dynamodb import ServiceResource


# https://github.com/boto/boto3/issues/369
def replace_decimals(obj):
    if isinstance(obj, list):
        for i, val in enumerate(obj):
            obj[i] = replace_decimals(val)
        return obj

    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj

    if isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)

        return float(obj)

    return obj


def get_dynamo_table():
    dynamodb: ServiceResource = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["DYNAMO_DB"])
    return table
