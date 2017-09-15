# -*- coding: utf-8 -*-

import mock
from nose.tools import (assert_false,
                        assert_in,
                        assert_is_not_none,
                        assert_not_in,
                        assert_true)

from .. import filters, flush_strategies


class TestNoDuplicateString(object):

    def __init__(self):
        self.string = self.duplicate = None

    def setup(self):
        self.string = self.duplicate = 'foo'

    def test_flush_strategy(self):
        flush_strategy = flush_strategies.AfterSize(maximum_size=1)
        filter_ = filters.NoDuplicateString(flush_strategy=flush_strategy)
        filter_.filter(string=self.string)
        string = filter_.filter(string=self.string)
        assert_is_not_none(string)

    def test_should_filter_unique_body_should_not_filter(self):
        filter_ = filters.NoDuplicateString(flush_strategy=None)
        filter_._should_filter(string=self.string)
        unique = 'bar'
        should_filter = filter_._should_filter(string=unique)
        assert_false(should_filter)

    def test_should_filter_duplicate_body_should_filter(self):
        filter_ = filters.NoDuplicateString(flush_strategy=None)
        filter_._should_filter(string=self.string)
        should_filter = filter_._should_filter(string=self.duplicate)
        assert_true(should_filter)


class TestLoggingString(object):

    def __init__(self):
        self.string = None
        self.logger = None
        self.string_filter = None

    def setup(self):
        self.string = 'foo'
        self.logger = mock.Mock()
        self.logger.debug = mock.Mock()

        flush_strategy = flush_strategies.AfterSize(maximum_size=2)
        string_filter = filters.NoDuplicateString(flush_strategy=flush_strategy)
        self.string_filter = filters.LoggingString(string_filter=string_filter,
                                                   logger=self.logger)

    def test_data_filtered_event_is_logged(self):
        kwargs = 1
        self.string_filter.filter(string=self.string)
        self.string_filter.filter(string=self.string)
        message = self.logger.debug.call_args[kwargs]['msg']
        assert_not_in('not', message)

    def test_data_not_filtered_event_is_logged(self):
        kwargs = 1
        self.string_filter.filter(string=self.string)
        message = self.logger.debug.call_args[kwargs]['msg']
        assert_in('not', message)
