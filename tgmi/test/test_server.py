"""
 Copyright (c) 2023 h3r0cybersec

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from unittest import main, skip
from tgmi.core.server import Route
from tgmi.toolbox.client import fetch
from tgmi.test.init import BaseTestServer

class TestServerIndex(BaseTestServer):
    def _registry_controller(self) -> None:
        class IndexRoute(Route):
            def __init__(self) -> None:
                super().__init__()
                self._routes = {
                    "/": "h_index"
                }
            def h_index(self):
                return self.response.success("index page")
        self.index_route = IndexRoute()
    
    def _registry_view(self) -> None:
        self.server.add_route(self.index_route)

    def test_index(self):
        """ is index reacheable?"""
        res = fetch("gemini://localhost/", store_out=True)
        self.assertEqual("20 text/gemini; charset=utf-8\r\nindex page\r\n", res)

class TestServerBadRequests(BaseTestServer):
    def _registry_controller(self) -> None:
        class BadRoute(Route):
            _routes = {
                "/invalid_url_len"  : "h_invalid_url_len",
                "/invalid_byte"     : "h_invalid_byte",
                "/invalid_schema"   : "h_invalid_schema",
                "/invalid_userinfo" : "h_invalid_userinfo"
            }

            def h_invalid_url_len(self):
                self.response.bad_request("uri to long")

            def h_invalid_byte(self):
                self.response.bad_request("invalid byte")

            def h_invalid_schema(self):
                self.response.bad_request("invalid schema")

            def h_invalid_userinfo(self):
                self.response.bad_request("userinfo is not allowed")

        self.bad_route = BadRoute()

    def _registry_view(self) -> None:
        self.server.add_route(self.bad_route)
    
    @skip("not implemented yet")
    def test_invalid_byte(self):
        """is url contains invalid bytes?"""
        pass
    
    def test_invalid_schema(self):
        """ is valid schema? """
        res = fetch("http://localhost/", store_out=True)
        self.assertEqual("59 not supported protocol\r\n", res)

    def test_invalid_userinfo(self):
        """ are userinfo in url? """
        res = fetch("gemini://test:test@localhost/", store_out=True)
        self.assertEqual("59 not allowed 'userinfo' for gemini protocol\r\n", res)

if __name__ == "__main__":
    main()