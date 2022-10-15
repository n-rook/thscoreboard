import unittest

from . import http_util


class HttpUtilTestCase(unittest.TestCase):

    def testGetDownloadFileHeaders_Ascii(self):
        headers = http_util.GetDownloadFileHeaders(
            ascii_filename='test123',
            full_filename='test123'
        )

        self.assertEqual(headers['Content-Type'], 'application/octet-stream')
        self.assertEqual(
            headers['Content-Disposition'],
            'attachment; filename="test123"; filename*=utf-8\'\'test123'
        )
    
    def testGetDownloadFileHeaders_Unicode(self):
        headers = http_util.GetDownloadFileHeaders(
            ascii_filename='test.rpy',
            full_filename='test_東方風神録.rpy'
        )

        self.assertEqual(headers['Content-Type'], 'application/octet-stream')
        self.assertEqual(
            headers['Content-Disposition'],
            'attachment; filename="test.rpy"; filename*=utf-8\'\'test_%E6%9D%B1%E6%96%B9%E9%A2%A8%E7%A5%9E%E9%8C%B2.rpy'
        )
