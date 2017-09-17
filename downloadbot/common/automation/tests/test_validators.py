# -*- coding: utf-8 -*-

import multiprocessing

import selenium.webdriver
from nose.tools import raises
from selenium.webdriver.support.wait import WebDriverWait

from .. import exceptions
from .. import validators
from ..compat import HttpStatus
from ..compat import http_serving

LOCALHOST = '127.0.0.1'
PORT_NUMBER = 9090


class MockServer(http_serving.BaseHTTPRequestHandler):

    _PAGES_INDEX = {'connection_lost':
"""
<body>
  <div class="ps-overlay">
    <div>
      <form>
        <p>disconnected</p>
      </form>
    </div>
  </div>
</body>
"""}

    def do_GET(self):
        try:
            page = self._PAGES_INDEX[self.path.lstrip('/').rstrip('/')]
        except KeyError:
            page = ''
            http_status = HttpStatus.INTERNAL_SERVER_ERROR
        else:
            http_status = HttpStatus.OK

        self.send_response(code=http_status)
        self.end_headers()
        self.wfile.write(page)


class TestPokemonShowdown(object):

    def __init__(self):
        self.process = None

        self.web_driver = None
        self.validator = None

    def setup(self):
        self.process = multiprocessing.Process(target=self.serve)
        self.process.start()

        chrome_options = selenium.webdriver.ChromeOptions()
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('headless')
        chrome_options.add_argument('no-sandbox')

        self.web_driver = selenium.webdriver.Chrome(
            chrome_options=chrome_options)
        wait_context = WebDriverWait(driver=self.web_driver, timeout=0)
        self.validator = validators.PokemonShowdown(wait_context=wait_context)

    @raises(exceptions.ConnectionLost)
    def test_connection_lost_raises_exception(self):
        self.initialize_web_driver(path='connection_lost')
        self.validator.check_connection_exists()

    def initialize_web_driver(self, path):
        url = self.build_url(path=path)
        self.web_driver.get(url=url)

    @staticmethod
    def build_url(path):
        template = 'http://{}:{}/{}/'
        url = template.format(LOCALHOST, PORT_NUMBER, path)
        return url

    @staticmethod
    def serve():
        server_address = (LOCALHOST, PORT_NUMBER)
        http_server = http_serving.HTTPServer(server_address=server_address,
                                              RequestHandlerClass=MockServer)
        http_server.serve_forever()

    def teardown(self):
        self.process.terminate()
