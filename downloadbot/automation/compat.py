# -*- coding: utf-8 -*-

import sys

_MAJOR_AND_MINOR = slice(0, 2)
_PYTHON_VERSION = sys.version_info[_MAJOR_AND_MINOR]
_PYTHON_VERSION_27 = (2, 7)
_PYTHON_VERSION_3 = (3, 0)

if _PYTHON_VERSION == _PYTHON_VERSION_27:
    import BaseHTTPServer as http_serving
    import httplib as HttpStatus
elif _PYTHON_VERSION >= _PYTHON_VERSION_3:
    import http.server as http_serving
    from http import HTTPStatus as HttpStatus
else:
    message = 'This version of Python is not compatible.'
    raise ImportError(message)
