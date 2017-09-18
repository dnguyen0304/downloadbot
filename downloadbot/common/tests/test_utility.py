# -*- coding: utf-8 -*-

import json

from nose.tools import assert_equal

from .. import utility


class MockException(Exception):
    pass


class TestFormatException(object):

    def __init__(self):
        self.message = None
        self.data = None

    def setup(self):
        self.message = 'foo'
        try:
            raise MockException(self.message)
        except MockException as e:
            formatted = utility.format_exception(e=e)
            self.data = json.loads(formatted)

    def test_formatted_includes_exception_type(self):
        assert_equal(self.data['exception_type'],
                     __name__ + '.' + MockException.__name__)

    def test_formatted_includes_exception_message(self):
        assert_equal(self.data['exception_message'], self.message)
