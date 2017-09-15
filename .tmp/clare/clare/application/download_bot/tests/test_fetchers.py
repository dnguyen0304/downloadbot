# -*- coding: utf-8 -*-

import itertools
import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import mock
from nose.tools import assert_equal, assert_false, assert_true, raises

from .. import fetchers
from clare.common import messaging


class TestBufferingFetcher(object):

    def __init__(self):
        self.queue = None
        self.countdown_timer = None
        self.maximum_message_count = None
        self.fetcher = None

    def setup(self):
        self.queue = queue.Queue()
        self.countdown_timer = self.create_mock_countdown_timer(
            has_time_remaining=itertools.repeat(True))
        self.maximum_message_count = 2
        self.fetcher = fetchers.BufferingFetcher(
            queue=self.queue,
            countdown_timer=self.countdown_timer,
            maximum_message_count=self.maximum_message_count)

    def test_pop_does_fetch_when_buffer_is_empty(self):
        side_effect = xrange(self.maximum_message_count)
        self.queue.get = mock.Mock(side_effect=side_effect)
        self.fetcher.pop(timeout=0.0)
        assert_true(self.queue.get.called)

    def test_pop_does_not_fetch_while_buffer_has_records(self):
        self.test_pop_does_fetch_when_buffer_is_empty()
        self.queue.get.reset_mock()
        self.fetcher.pop(timeout=0.0)
        assert_false(self.queue.get.called)

    def test_pop_minimum_message_count_with_time_remaining(self):
        fetcher = self.create_fetcher_for_minimum_message_count(
            has_time_remaining=(True, False))
        fetcher.pop(timeout=0.0)

    def test_pop_minimum_message_count_with_no_time_remaining(self):
        fetcher = self.create_fetcher_for_minimum_message_count(
            has_time_remaining=(False,))
        fetcher.pop(timeout=0.0)

    def test_pop_is_ordered(self):
        expected = list()
        records = list()
        # These loops cannot be merged because there are not enough
        # messages enqueued for the buffer.
        for i in xrange(self.maximum_message_count):
            expected.append(i)
            self.queue.put(i)
        for i in xrange(self.maximum_message_count):
            record = self.fetcher.pop(timeout=0.0)
            records.append(record)
        assert_equal(records, expected)

    @raises(messaging.consumer.exceptions.FetchTimeout)
    def test_pop_timeout_raises_exception(self):
        self.countdown_timer = self.create_mock_countdown_timer(
            has_time_remaining=(False,))
        fetcher = fetchers.BufferingFetcher(
            queue=self.queue,
            countdown_timer=self.countdown_timer,
            maximum_message_count=self.maximum_message_count)
        fetcher.pop(timeout=0.0)

    def test_pop_timeout_resets_countdown_timer(self):
        self.test_pop_timeout_raises_exception()
        assert_true(self.countdown_timer.reset.called)

    @staticmethod
    def create_mock_countdown_timer(has_time_remaining):

        """
        Parameters
        ----------
        has_time_remaining : collections.Iterable

        Returns
        -------
        mock.Mock
        """

        mock_countdown_timer = mock.Mock()
        has_time_remaining = mock.PropertyMock(side_effect=has_time_remaining)
        type(mock_countdown_timer).has_time_remaining = has_time_remaining
        return mock_countdown_timer

    def create_fetcher_for_minimum_message_count(self, has_time_remaining):

        """
        Parameters
        ----------
        has_time_remaining : collections.Iterable

        Returns
        -------
        clare.application.download_bot_fetcher.BufferingFetcher
        """

        for i in xrange(self.maximum_message_count - 1):
            self.queue.put(i)
        countdown_timer = self.create_mock_countdown_timer(
            has_time_remaining=has_time_remaining)
        fetcher = fetchers.BufferingFetcher(
            queue=self.queue,
            countdown_timer=countdown_timer,
            maximum_message_count=self.maximum_message_count)
        return fetcher
