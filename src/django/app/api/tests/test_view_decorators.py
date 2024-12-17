
import unittest
from collections import namedtuple
from api.view_decorators import service_proxy_error
from requests.exceptions import HTTPError

MockResp = namedtuple("mock_resp",("content","status_code"))

class TestDecs(unittest.TestCase):
    def test_service_proxy(self):
        @service_proxy_error
        def fails():
            mock_resp = MockResp(content="yoo",status_code=500)
            raise HTTPError(response=mock_resp)
        rsp = fails()
        self.assertEqual(rsp.status_code,500)
        self.assertEqual(rsp.content,b"yoo")
