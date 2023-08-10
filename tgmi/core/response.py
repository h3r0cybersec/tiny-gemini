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

from typing import Union, NamedTuple, Tuple
from pathlib import Path
from enum import IntEnum, unique

@unique
class StatusCode(IntEnum):
    """
        Codici di stato protocollo Gemini
    """
    INPUT                       = 10
    SENSITIVE_INPUT             = 11
    SUCCESS                     = 20
    TEMPORARY_REDIRECT          = 30
    PERMANENT_REDIRECT          = 31
    TEMPORARY_FAILURE           = 40
    SERVER_UNAVAILABLE          = 41
    CGI_ERROR                   = 42
    PROXY_ERROR                 = 43
    SLOW_DOWN                   = 44
    PERMANENT_FAILURE           = 50
    NOT_FOUND                   = 51
    GONE                        = 52
    PROXY_REQUEST_REFUSED       = 53
    BAD_REQUEST                 = 59
    CLIENT_CERTIFICATE_REQUIRED = 60                
    CERTIFICATE_NOT_AUTHORIZED  = 61
    CERTIFICATE_NOT_VALID       = 62

class Response:
    """
        Response object.
        Official specification
         => https://gemini.circumlunar.space/docs/specification.gmi
            sec: 3.1
        TODO: implement other response and make sure that all response follow
              right logics as to protocol specification 
    """

    class ProxyResponse(NamedTuple):
        status   : int              = 20
        meta     : Union[str, Path] = ""
        mime     : str              = "text/gemini; charset=utf-8"

        @property
        def end(self) -> str:
            if self.status in [
                StatusCode.INPUT, 
                StatusCode.SENSITIVE_INPUT,
                StatusCode.TEMPORARY_FAILURE,
                StatusCode.TEMPORARY_REDIRECT,
                StatusCode.PERMANENT_REDIRECT,
                StatusCode.PERMANENT_FAILURE,
                StatusCode.NOT_FOUND,
                StatusCode.BAD_REQUEST
            ]:
                return f"{self.status} {self.meta}\r\n"
            return f"{self.status} {self.mime}\r\n{self.meta}\r\n"

    @classmethod    
    def input(cls, meta: str) -> ProxyResponse:
        """
            Richiesto input
        """
        return cls.ProxyResponse(StatusCode.INPUT, meta)
    
    @classmethod
    def sensitive_input(cls, meta: str) -> ProxyResponse:
        return cls.ProxyResponse(StatusCode.SENSITIVE_INPUT, meta)

    @classmethod
    def success(cls, meta: Union[str, Tuple[str, str]]) -> ProxyResponse:
        if isinstance(meta, tuple):
            meta, mime = meta
            if mime:
                return cls.ProxyResponse(StatusCode.SUCCESS, meta, mime)
            else:
                return cls.ProxyResponse(StatusCode.SUCCESS, meta)
        else:
            return cls.ProxyResponse(StatusCode.SUCCESS, meta)

    @classmethod
    def not_found(cls, meta: str) -> ProxyResponse:
        return cls.ProxyResponse(StatusCode.NOT_FOUND, meta)
    
    @classmethod
    def bad_request(cls, meta: str) -> ProxyResponse:
        return cls.ProxyResponse(StatusCode.BAD_REQUEST, meta)
    
    @classmethod
    def temporary_redirect(cls, to: str) -> ProxyResponse:
        return cls.ProxyResponse(StatusCode.TEMPORARY_REDIRECT, to)

    @classmethod
    def temporary_failure(cls, meta: str):
        return cls.ProxyResponse(StatusCode.TEMPORARY_FAILURE, meta)

    @classmethod
    def permanent_redirect(cls, to: str):
        return cls.ProxyResponse(StatusCode.PERMANENT_REDIRECT, to)
    
    @classmethod
    def permanent_failure(cls, meta: str):
        return cls.ProxyResponse(StatusCode.PERMANENT_FAILURE, meta)

    @classmethod
    def client_certficate_required(cls):
        raise NotImplementedError
    
    @classmethod
    def server_unavailable(cls):
        return cls.ProxyResponse(StatusCode.SERVER_UNAVAILABLE)