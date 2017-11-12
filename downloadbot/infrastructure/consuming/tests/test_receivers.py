# -*- coding: utf-8 -*-

import collections
import itertools
import queue

import mock
from nose.tools import assert_equal, assert_raises, assert_true, raises

from .. import receivers
from downloadbot.common import messaging
from downloadbot.common.messaging import consuming


class MockSqsMessage:

    def __init__(self, message_id, body, receipt_handle):
        self.message_id = message_id
        self.body = body
        self.receipt_handle = receipt_handle

    @classmethod
    def from_message(cls, message):

        """
        Message adapter.

        Parameters
        ----------
        message : downloadbot.common.messaging.messages.Message
        """

        return cls(message_id=message.id,
                   body=message.body,
                   receipt_handle=message.delivery_receipt)


class MockSqsQueue:

    def receive_messages(self):
        pass


class TestReceiver:

    def __init__(self):
        self._buffer = collections.deque()
        self.data = None
        self.messages = list()
        self.message = None

    def setup(self):
        self.data = ('foo', 'bar', 'foobar')
        for x in self.data:
            message = messaging.messages.Message(id=None,
                                                 body=x,
                                                 delivery_receipt=None)
            self.messages.append(message)
        self.message = self.messages[0]


class TestConcurrentLinkedQueue(TestReceiver):

    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()

    def test_receive_does_fill_if_buffer_is_empty(self):
        batch_size_maximum_count = 1
        countdown_timer = TestConcurrentLinkedQueue.create_mock_countdown_timer(
            has_time_remaining=itertools.repeat(True))
        receiver = receivers.ConcurrentLinkedQueue(
            queue=self.queue,
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            _buffer=self._buffer)

        for x in self.data:
            self.queue.put(x)
        expected_queue_count = self.queue.qsize() - batch_size_maximum_count
        message = receiver.receive()

        assert_equal(expected_queue_count, self.queue.qsize())
        assert_equal(batch_size_maximum_count - 1, len(self._buffer))
        assert_equal(self.message.body, message.body)

        assert_true(countdown_timer.reset.called)

    def test_receive_does_not_fill_if_buffer_has_messages(self):
        self._buffer.append(self.message)
        receiver = receivers.ConcurrentLinkedQueue(
            queue=self.queue,
            batch_size_maximum_count=None,
            countdown_timer=None,
            _buffer=self._buffer)
        expected_buffer_count = len(self._buffer) - 1

        for x in self.data:
            self.queue.put(x)
        message = receiver.receive()

        assert_equal(len(self.messages), self.queue.qsize())
        assert_equal(expected_buffer_count, len(self._buffer))
        assert_equal(self.message.body, message.body)

    def test_receive_timeout_raises_exception(self):
        batch_size_maximum_count = 1
        countdown_timer = TestConcurrentLinkedQueue.create_mock_countdown_timer(
            has_time_remaining=(False,))
        receiver = receivers.ConcurrentLinkedQueue(
            queue=self.queue,
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer)

        assert_raises(consuming.exceptions.ReceiveTimeout, receiver.receive)

        assert_true(countdown_timer.reset.called)

    def test_receive_is_ordered(self):
        batch_size_maximum_count = len(self.messages)
        countdown_timer = TestConcurrentLinkedQueue.create_mock_countdown_timer(
            has_time_remaining=itertools.repeat(True))
        receiver = receivers.ConcurrentLinkedQueue(
            queue=self.queue,
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer)

        for x in self.data:
            self.queue.put(x)
        for expected_message in self.messages:
            message = receiver.receive()
            assert_equal(expected_message.body, message.body)

        assert_true(countdown_timer.reset.called)

    @staticmethod
    def create_mock_countdown_timer(has_time_remaining):

        """
        Parameters
        ----------
        has_time_remaining : typing.Iterable

        Returns
        -------
        mock.Mock
        """

        mock_countdown_timer = mock.Mock()
        type(mock_countdown_timer).has_time_remaining = mock.PropertyMock(
            side_effect=has_time_remaining)
        mock_countdown_timer.reset = mock.Mock()
        return mock_countdown_timer


class TestSqsFifo(TestReceiver):

    def test_receive_does_fill_if_buffer_is_empty(self):
        return_value = [MockSqsMessage.from_message(self.message)]
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=return_value)
        receiver = receivers.SqsFifoQueue(sqs_queue=sqs_queue,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None)
        message = receiver.receive()
        assert_equal(self.message.body, message.body)

    def test_receive_does_not_fill_if_buffer_has_messages(self):
        self._buffer.append(self.message)
        receiver = receivers.SqsFifoQueue(sqs_queue=None,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None,
                                          _buffer=self._buffer)
        message = receiver.receive()
        assert_equal(self.message.body, message.body)

    @raises(consuming.exceptions.ReceiveTimeout)
    def test_receive_timeout_raises_exception(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=list())
        receiver = receivers.SqsFifoQueue(sqs_queue=sqs_queue,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None)
        receiver.receive()
