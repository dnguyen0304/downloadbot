# -*- coding: utf-8 -*-

import Queue as queue
import collections
import uuid

from clare.common.messaging import consumer


class ConcurrentLinkedQueue(consumer.receivers.Receiver):

    def __init__(self,
                 queue,
                 batch_size_maximum_count,
                 countdown_timer,
                 message_factory,
                 _buffer=None):

        """
        Parameters
        ----------
        queue : Queue.Queue
        batch_size_maximum_count : int
            Maximum size of the batch. The units are in number of
            messages.
        countdown_timer : clare.common.utilities.timers.CountdownTimer
        message_factory : clare.common.messaging.factories.Message
        """

        self._queue = queue
        self._batch_size_maximum_count = batch_size_maximum_count
        self._countdown_timer = countdown_timer
        self._message_factory = message_factory

        self._buffer = _buffer if _buffer is not None else collections.deque()

    def receive(self):
        if not self._buffer:
            self._fill_buffer()
        try:
            message = self._buffer.popleft()
        except IndexError:
            message = 'The receive operation timed out.'
            raise consumer.exceptions.ReceiveTimeout(message)
        return message

    def _fill_buffer(self):
        data = list()
        self._countdown_timer.start()

        while True:
            # This must run at least once (i.e. do-while semantics).
            try:
                x = self._queue.get(block=False)
            except queue.Empty:
                pass
            else:
                data.append(x)

            if len(data) == self._batch_size_maximum_count:
                break
            if not self._countdown_timer.has_time_remaining:
                break

        self._countdown_timer.reset()

        for x in data:
            message = self._message_factory.create()

            message.id = str(uuid.uuid4())
            message.body = str(x)
            message.delivery_receipt = str(uuid.uuid4())

            self._buffer.append(message)

    def __repr__(self):
        repr_ = ('{}('
                 'queue={}, '
                 'batch_size_maximum_count={}, '
                 'countdown_timer={}, '
                 'message_factory={})')
        return repr_.format(self.__class__.__name__,
                            self._queue,
                            self._batch_size_maximum_count,
                            self._countdown_timer,
                            self._message_factory)


class SqsFifoQueue(consumer.receivers.Receiver):

    def __init__(self,
                 sqs_queue,
                 batch_size_maximum_count,
                 wait_time_seconds,
                 message_factory,
                 _buffer=None):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        batch_size_maximum_count : int
            Maximum size of the batch. The units are in number of
            messages.
        wait_time_seconds : int
            Duration for which to wait. The units are in seconds.
        message_factory : clare.common.messaging.factories.Message
        """

        self._sqs_queue = sqs_queue
        self._batch_size_maximum_count = batch_size_maximum_count
        self._wait_time_seconds = wait_time_seconds
        self._message_factory = message_factory

        self._buffer = _buffer if _buffer is not None else collections.deque()

    def receive(self):
        if not self._buffer:
            self._fill_buffer()
        try:
            message = self._buffer.popleft()
        except IndexError:
            message = 'The receive operation timed out.'
            raise consumer.exceptions.ReceiveTimeout(message)
        return message

    def _fill_buffer(self):
        messages = self._sqs_queue.receive_messages(
            MaxNumberOfMessages=self._batch_size_maximum_count,
            WaitTimeSeconds=self._wait_time_seconds)

        for message in messages:
            marshalled = self._message_factory.create()

            marshalled.id = message.message_id
            marshalled.body = message.body
            marshalled.delivery_receipt = message.receipt_handle

            self._buffer.append(marshalled)

    def __repr__(self):
        repr_ = ('{}('
                 'sqs_queue={}, '
                 'batch_size_maximum_count={}, '
                 'wait_time_seconds={}, '
                 'message_factory={})')
        return repr_.format(self.__class__.__name__,
                            self._sqs_queue,
                            self._batch_size_maximum_count,
                            self._wait_time_seconds,
                            self._message_factory)
