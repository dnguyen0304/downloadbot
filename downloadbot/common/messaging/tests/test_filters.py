# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_in, assert_not_in

from .. import filters
from .. import messages


class TestLogging:

    def __init__(self):
        self.message = None
        self.logger = None

    def setup(self):
        self.message = messages.Message(id='', body='', delivery_receipt='')
        self.logger = mock.Mock()
        self.logger.debug = mock.Mock()

    def test_data_filtered_event_is_logged(self):
        message_filter = mock.Mock()
        message_filter.filter = mock.Mock(return_value=None)
        message_filter = filters.Logging(message_filter=message_filter,
                                         logger=self.logger)

        kwargs = 1

        message_filter.filter(message=self.message)
        output = self.logger.debug.call_args[kwargs]['msg']
        assert_not_in('not', output)

    def test_data_not_filtered_event_is_logged(self):
        message_filter = mock.Mock()
        message_filter.filter = mock.Mock(return_value=self.message)
        message_filter = filters.Logging(message_filter=message_filter,
                                         logger=self.logger)

        kwargs = 1

        message_filter.filter(message=self.message)
        output = self.logger.debug.call_args[kwargs]['msg']
        assert_in('not', output)
