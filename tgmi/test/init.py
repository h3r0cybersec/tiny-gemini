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

from abc import ABCMeta, abstractmethod
from unittest import TestCase
from threading import Thread
from tgmi.core.server import GeminiServer
from time import sleep

class BaseTestServer(TestCase, metaclass=ABCMeta):

    @abstractmethod
    def _registry_controller(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _registry_view(self) -> None:
        raise NotImplementedError
    
    def setUp(self) -> None:
        self.server = GeminiServer()
        self._registry_controller()
        self._registry_view()
        self.bg = Thread(target=self.server.serve_forever)
        self.bg.daemon = True
        self.bg.start()

    def tearDown(self) -> None:
        self.server.server_close()
        self.server.shutdown()
        sleep(0.5)
