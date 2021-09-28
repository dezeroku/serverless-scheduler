# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.compare_request import CompareRequest  # noqa: E501
from swagger_server.models.compare_response import CompareResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_compare(self):
        """Test case for compare

        returns score and picture diff of provided images
        """
        return
        body = CompareRequest()
        response = self.client.open(
            '/dezeroku/monitor-page-comparator/1.0.0/compare',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
