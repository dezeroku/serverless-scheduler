# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.screenshot import Screenshot  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_screenshot(self):
        """Test case for screenshot

        gets screenshot of provided URL
        """
        return
        query_string = [('url', 'url_example')]
        response = self.client.open(
            '/d0ku/monitor-screenshoter/1.0.0/screenshot',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
