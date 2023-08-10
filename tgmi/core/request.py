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

from urllib.parse import urlsplit, urlunsplit, parse_qs
from tgmi.utils import escape
from tgmi.core.exception import (
    GeminiBadRequestError
)

class Request:
    """
        Request object
    """
    def __init__(self, remote_client: str, path: bytes) -> None:
        self._remote_client = remote_client
        self._resource  = urlsplit(escape(path))
        self._scheme    = self._resource.scheme.decode()
        self._domain    = self._resource.netloc.decode()
        self._path      = self._resource.path.decode()
        self._query     = self._resource.query.decode()
        self._fragment  = self._resource.fragment.decode()

    @property
    def remote_client(self) -> str:
        """
            show remote ip
        """
        return self._remote_client

    @property
    def url(self) -> str:
        """
            show origin url
        """
        return urlunsplit(self._resource).decode()
    
    @property
    def scheme(self) -> str:
        """
            show request protocol
        """
        return self._scheme

    @property
    def domain(self) -> str:
        """
            show domain
        """
        return self._domain

    @property
    def path(self) -> str:
        """
            show requested path
        """
        return self._path

    @property
    def query(self) -> str:
        """
            show query params
        """
        if self._query:
            return list(parse_qs(self._query, keep_blank_values=True).keys())[0]
        else:
            return self._query

    @property
    def fragment(self) -> str:
        """
            show path fragments
        """
        return self._fragment

    def is_valid_uri(self) -> bool:
        """
            Check if uri is compliant to Gemini protocol:
                => ref: https://gemini.circumlunar.space/docs/specification.gmi
                => sec: 2 Gemini Request
            TODO: All protocol specs have been implemented ?
        """
        # 1. uri length should be less then 1024
        if 0 < len(urlunsplit(self._resource).decode()) <= 1024:
            # 2. uri shouldn't include initial U+FEFF bytes
            if self._domain[0:2] != b"\xfe\xff":
                #3. protocol schema should be 'gemini://'
                if self._scheme == "gemini":
                    #4. uri shouldn't contains 'userinfo' section
                    if self._resource.username is None and self._resource.password is None:
                        return True
                    else:
                        raise GeminiBadRequestError("not allowed 'userinfo' for gemini protocol")
                else: 
                    raise GeminiBadRequestError("not supported protocol")
            else:
                raise GeminiBadRequestError("invalid bytes")
        else:
            raise GeminiBadRequestError("exceded uri length")        

    def __str__(self) -> str:
        return f"<Request {self.url}>"
    