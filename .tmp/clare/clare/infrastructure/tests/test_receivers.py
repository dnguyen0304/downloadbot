# -*- coding: utf-8 -*-

import Queue as queue
import collections
import itertools

import mock
from nose.tools import assert_equal, assert_raises, assert_true, raises

from .. import receivers
from .. import senders
from clare.common.messaging import consumer
from clare.common.messaging import factories


class MockSqsMessage(object):

    def __init__(self, message_id, body, receipt_handle):

        """
        Parameters
        ----------
        message_id : str
            Unique identifier.
        body : str
            Content.
        receipt_handle : str
            Unique identifier associated with the transaction of
            receiving this message.
        """

        self.message_id = message_id
        self.body = body
        self.receipt_handle = receipt_handle

    @classmethod
    def from_message(cls, message):

        """
        Parameters
        ----------
        message : clare.common.messaging.models.Message
        """

        return cls(message_id=message.id,
                   body=message.body,
                   receipt_handle=message.delivery_receipt)

    def __repr__(self):
        repr_ = '{}(message_id="{}", body="{}", receipt_handle="{}")'
        return repr_.format(self.__class__.__name__,
                            self.message_id,
                            self.body,
                            self.receipt_handle)


class MockSqsQueue(object):

    def receive_messages(self):
        pass


class TestReceiver(object):

    def setup(self):
        self.message_factory = factories.Message2()
        self._buffer = collections.deque()

        self.data = ('foo', 'bar', 'foobar')
        self.messages = list()
        for x in self.data:
            message = self.message_factory.create()

            message.id = None
            message.body = x
            message.delivery_receipt = None

            self.messages.append(message)
        self.message = self.messages[0]


class TestConcurrentLinkedDeque(TestReceiver):

    def setup(self):
        super(TestConcurrentLinkedDeque, self).setup()

        self.queue = queue.Queue()
        self.sender = senders.ConcurrentLinkedQueue(queue=self.queue)

    def test_receive_does_fill_when_buffer_is_empty(self):
        batch_size_maximum_count = 1
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=itertools.repeat(True))

        receiver = receivers.ConcurrentLinkedQueue(
            queue=self.queue,
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=self.message_factory,
            _buffer=self._buffer)

        for x in self.data:
            self.sender.send(x)
        expected_queue_count = self.queue.qsize() - batch_size_maximum_count
        message = receiver.receive()

        assert_equal(expected_queue_count, self.queue.qsize())
        assert_equal(batch_size_maximum_count - 1, len(self._buffer))
        assert_equal(self.message.body, message.body)

        assert_true(countdown_timer.reset.called)

    def test_receive_does_not_fill_while_buffer_has_messages(self):
        self._buffer.append(self.message)

        receiver = receivers.ConcurrentLinkedQueue(
            queue=self.queue,
            batch_size_maximum_count=None,
            countdown_timer=None,
            message_factory=None,
            _buffer=self._buffer)

        expected_buffer_count = len(self._buffer) - 1

        for x in self.data:
            self.sender.send(x)
        message = receiver.receive()

        assert_equal(len(self.messages), self.queue.qsize())
        assert_equal(expected_buffer_count, len(self._buffer))
        assert_equal(self.message.body, message.body)

    def test_receive_timeout_raises_exception(self):
        batch_size_maximum_count = 1
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=(False,))

        receiver = receivers.ConcurrentLinkedQueue(
            queue=self.queue,
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=None)

        assert_raises(consumer.exceptions.ReceiveTimeout, receiver.receive)

        assert_true(countdown_timer.reset.called)

    def test_receive_is_ordered(self):
        batch_size_maximum_count = len(self.messages)
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=itertools.repeat(True))

        receiver = receivers.ConcurrentLinkedQueue(
            queue=self.queue,
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=self.message_factory)

        for x in self.data:
            self.sender.send(x)
        for expected_message in self.messages:
            message = receiver.receive()
            assert_equal(expected_message.body, message.body)

        assert_true(countdown_timer.reset.called)

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
        type(mock_countdown_timer).has_time_remaining = mock.PropertyMock(
            side_effect=has_time_remaining)
        mock_countdown_timer.reset = mock.Mock()
        return mock_countdown_timer


class TestSqsFifo(TestReceiver):

    def test_receive_does_fill_when_buffer_is_empty(self):
        return_value = [MockSqsMessage.from_message(self.message)]
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=return_value)

        receiver = receivers.SqsFifoQueue(sqs_queue=sqs_queue,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None,
                                          message_factory=self.message_factory)
        message = receiver.receive()
        assert_equal(self.message.body, message.body)

    def test_receive_does_not_fill_while_buffer_has_messages(self):
        self._buffer.append(self.message)

        receiver = receivers.SqsFifoQueue(sqs_queue=None,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None,
                                          message_factory=None,
                                          _buffer=self._buffer)
        message = receiver.receive()
        assert_equal(self.message.body, message.body)

    @raises(consumer.exceptions.ReceiveTimeout)
    def test_receive_timeout_raises_exception(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=list())

        receiver = receivers.SqsFifoQueue(sqs_queue=sqs_queue,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None,
                                          message_factory=None)
        receiver.receive()
