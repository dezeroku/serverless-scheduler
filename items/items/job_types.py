import logging

from common.models.plugins import PLUGINS_ALL_CLASSES_LIST
from items.libs.lambda_decorators import cors_headers, json_http_resp

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cors_headers
@json_http_resp
def get(event, context) -> dict:
    # pylint: disable=unused-argument
    return handler()


def handler() -> list[dict]:
    # Get all the classes from plugins and
    # report their schemas as a list
    return list(map(lambda x: x.schema(), PLUGINS_ALL_CLASSES_LIST))
