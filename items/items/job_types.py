import logging

from common.models.plugins import PLUGINS_CLASS_MAPPING
from items.libs.lambda_decorators import cors_headers, json_http_resp

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cors_headers
@json_http_resp
def get(event, context) -> dict:
    # pylint: disable=unused-argument
    return handler()


def handler() -> dict:
    # Get all the classes from plugins and
    # report their schemas as a list
    return {k.value: v.schema() for k, v in PLUGINS_CLASS_MAPPING.items()}
