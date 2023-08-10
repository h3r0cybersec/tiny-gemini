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

import socketserver as ss
import ssl
from datetime import datetime
from dataclasses import dataclass
from typing import Callable, Union, Dict
from pathlib import Path
from mimetypes import guess_type
from tgmi import log
from tgmi.core.request import Request
from tgmi.core.response import Response
from tgmi.core.exception import (
    GeminiBadRequestError,
    GeminiFileNotFoundError,
    GeminiFileNotSupportedError
)

class Route:
    """
        Route on server.
        TODO: handle dynamic parameters
    """
    _routes : Dict[str, str]

    def __init__(self) -> None:
        self._server      = GeminiServer       # TODO: Is really required? Is there a better way to gather only informations we need 
        self._request     = Request            # updated with current request after on [server.py:184]
        self._response    = Response

    @property
    def server(self) -> type:
        return self._server

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, r: Request):
        self._request = r

    @property
    def response(self) -> type:
        return self._response
    
    @property
    def routes(self):
        return self._routes

    def __interpolate_params(self, source: str, mime: Union[str, None], params: dict) -> tuple:
        """
            simplyfied engine that substitute placeholder with this syntax : ((placeholder))
            with the corrisponding values submitted in rendering methods inside 'params'
            TODO: Could be useful use Jinja instead ?
        """
        if len(params) > 0:
            for param, value in params.items():
                source = source.replace(f"(({param}))", value)
        return source, mime 

    def serve(self) -> Callable:
        """
            serve specifics request
        """
        available_handlers = [h for h in dir(self) if h.startswith("h_")]
        for r in self._routes.values():
            if r in available_handlers:
                # call specific method
                return getattr(self, r)()
        else:
            raise Exception(f"No handler was found to handle this request")
        
    def render_resource(self, resource: str, params: dict = {}) -> Union[tuple, None]:
        """
            render a file.
        """
        file_folder = self._server.get_cfgs()["PUBLIC_FOLDER"] / resource
        if Path(file_folder).exists():
            mime, _ = guess_type(file_folder)
            with open(file_folder) as file:
                content = file.read()
                return self.__interpolate_params(content, mime, params)
        else:
            raise Exception("resource provided was not found on this server")
        
    def __str__(self) -> str:
        return f"<Route({self.__class__.__name__}) [{','.join(self._routes.keys())}]>"

class GeminiServer(ss.ThreadingMixIn, ss.TCPServer):
    """
        Gemini Server
    """

    allow_reuse_address     : bool  = True
    buffer                  : int   = 1024
    default_configurations  : dict  = {
        "HOST"          : "127.0.0.1",
        "PORT"          : 1965,
        "PUBLIC_FOLDER" : Path().cwd() / "public",
        "SERVER_CRT"    : Path("../certs/server.crt"),
        "SERVER_KEY"    : Path("../certs/server.key"),
        "CLIENT_CRT"    : Path("../certs/client.crt")
    }
    
    @dataclass(frozen=True)
    class meta:
        """
            server metadata
        """
        _version : str   = f"Tgmi v0.1"

        @classmethod
        def version(cls):
            return cls._version
        
    def __init__(self, configurations : dict = {}):
        if configurations:
            for conf in configurations.keys():
                if conf not in self.default_configurations.keys():
                    raise ValueError(f"'{conf}' is not a valid configuration")
                else:
                    self.default_configurations[conf] = configurations[conf]

        super().__init__(
            (   
                self.default_configurations["HOST"], 
                self.default_configurations["PORT"]
            ),
            GeminiServerHandler
        )

        self.secure_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.secure_ctx.verify_mode = ssl.CERT_REQUIRED
        self.secure_ctx.load_cert_chain(certfile=self.default_configurations["SERVER_CRT"], keyfile=self.default_configurations["SERVER_KEY"])
        self.secure_ctx.load_verify_locations(cafile=self.default_configurations["CLIENT_CRT"])

        # registered routes 
        self.routes: list[Route] = []
    
    @classmethod
    def get_cfgs(cls):
        """
            ritorna le configurazioni del server
        """
        return cls.default_configurations

    def get_request(self):
        """
            Elabora la richiesta in arrivo
        """
        channel, client_sock = self.socket.accept()
        secure_channel = self.secure_ctx.wrap_socket(
            channel,
            server_side=True
        )
        return secure_channel, client_sock

    def server_activate(self) -> None:
        super().server_activate()
        log.info(f"[*] Server is listen on gemini://{self.server_address[0]}:{self.server_address[1]}")

    def add_route(self, handler: Route) -> None:
        """
            registry new route
        """
        log.debug(f"[+] Added router: {handler}")
        return self.routes.append(
            handler
        ) 

    def serve_resource(self, request: Request) -> Union[Callable, Response.ProxyResponse]:
        """
            serve a route
        """
        try:
            if request.is_valid_uri():
                for i, r in enumerate(self.routes):
                    if request.path in r.routes.keys():
                        route = self.routes[i]
                        route.request = request
                        return route.serve()
                else:
                    # no matching route
                    raise GeminiFileNotFoundError(f"request '{request.path}' was not found on this server")
            else:
                raise GeminiBadRequestError("bad request")
        except GeminiFileNotSupportedError as file_not_supported_error:
            return Response.permanent_failure(str(file_not_supported_error))
        except GeminiFileNotFoundError as file_not_found_error:
            return Response.not_found(str(file_not_found_error))
        except GeminiBadRequestError as bad_request_error:
            return Response.bad_request(str(bad_request_error))
        except Exception as general_error:
            return Response.permanent_failure(f"server error {general_error}")

class GeminiServerHandler(ss.StreamRequestHandler):
    """
        Handle server requests
    """
    def handle(self) -> None:
        """
            Handle a single request in a new Thread 
        """
        # read requested data
        data: bytes                  = self.rfile.readline(self.server.buffer).strip()
        # parse request
        req : Request                = Request(self.client_address, data)
        # compute response
        res : Response.ProxyResponse = self.server.serve_resource(req)
        # log request on stdout
        log.info(f"{datetime.now()} - {req.remote_client[0]} - {req.path} - status: {res.status}")
        # send response
        self.wfile.write(res.end.encode())