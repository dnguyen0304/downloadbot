# -*- coding: utf-8 -*-

import sys

_MAJOR_AND_MINOR = slice(0, 2)
_PYTHON_VERSION = sys.version_info[_MAJOR_AND_MINOR]
_PYTHON_VERSION_27 = (2, 7)

if _PYTHON_VERSION == _PYTHON_VERSION_27:
    import BaseHTTPServer as http_serving
    import httplib as HttpStatus
else:
    import http.server as http_serving
    import http.HTTPStatus as HttpStatus
