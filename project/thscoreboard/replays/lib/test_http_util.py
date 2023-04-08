import unittest

from . import http_util


class HttpUtilTestCase(unittest.TestCase):
    def testGetDownloadFileHeaders(self):
        headers = http_util.GetDownloadFileHeaders("test123")

        self.assertEqual(headers["Content-Type"], "application/octet-stream")
        self.assertEqual(
            headers["Content-Disposition"], 'attachment; filename="test123"'
        )
