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

from unittest import TestCase, main, skip
from tgmi.core.response import Response

class Test_Response(TestCase):
    """
        Testa le risposte del server
    """

    def test_input(self):
        res : Response.ProxyResponse = Response.input("account?")
        self.assertEqual("10 account?\r\n", res.end)

    def test_sensitive_input(self):
        res : Response.ProxyResponse = Response.sensitive_input("password?")
        self.assertEqual("11 password?\r\n", res.end)

    def test_success(self):
        res : Response.ProxyResponse = Response.success("test")
        self.assertEqual("20 text/gemini; charset=utf-8\r\ntest\r\n", res.end)

    def test_temporary_redirect(self):
        res : Response.ProxyResponse = Response.temporary_redirect("gemini://localhost/")
        self.assertEqual("30 gemini://localhost/\r\n", res.end)

    def test_permanent_redirect(self):
        res : Response.ProxyResponse = Response.permanent_redirect("gemini://localhost/test.gmi")
        self.assertEqual("31 gemini://localhost/test.gmi\r\n", res.end)

    def test_temporary_failure(self):
        pass

    def test_server_unavailable(self):
        pass
    
    @skip("not implemented yet")
    def test_cgi_error(self):
        pass
    
    @skip("not implemented yet")
    def test_proxy_error(self):
        pass

    @skip("not implemented yet")
    def test_slow_down(self):
        pass

    def test_permanent_failure(self):
        pass

    def test_not_found(self):
        pass

    @skip("not implemented yet")
    def test_gone(self):
        pass
    
    @skip("not implemented yet")
    def test_proxy_request_refused(self):
        pass

    def test_bad_request(self):
        pass
    
    @skip("not implemented yet")
    def test_client_certificate_required(self):
        pass
    
    @skip("not implemented yet")
    def test_certificate_not_authorized(self):
        pass
    
    @skip("not implemented yet")
    def test_certificate_not_valid(self):
        pass

if __name__ == '__main__':
    main()