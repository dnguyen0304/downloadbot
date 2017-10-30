# -*- coding: utf-8 -*-

from nose.tools import raises

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
