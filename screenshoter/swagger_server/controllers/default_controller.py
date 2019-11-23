import connexion
import six
import random
import string
import base64

from flask import jsonify

from swagger_server.models.screenshot import Screenshot  # noqa: E501
from swagger_server import util
from swagger_server import selenium_screenshot


def screenshot(url):  # noqa: E501
    """gets screenshot of provided URL

     # noqa: E501

    :param url: URL of the page you want to take a screenshot of
    :type url: str

    :rtype: Screenshot
    """
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits,
                                      k=8)) + ".png"
    selenium_screenshot.screenshot_url(url, filename)
    with open(filename, 'rb') as f:
            data = f.read()
            f.close()
    encoded = base64.b64encode(data).decode()

    response = {"image": encoded}

    return jsonify(response)
