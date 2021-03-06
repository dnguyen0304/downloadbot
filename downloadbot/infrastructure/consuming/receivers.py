# -*- coding: utf-8 -*-

import abc
import collections
import queue
import uuid
from http import HTTPStatus as HttpStatus

from downloadbot.common import io
from downloadbot.common import messaging
from downloadbot.common import utility
from downloadbot.common.messaging import consuming


class Disposable(consuming.receivers.Receiver, io.Disposable, metaclass=abc.ABCMeta):
    pass


class BaseBuffering(Disposable, metaclass=abc.ABCMeta):

    """
    Classes implementing this abstract base class must define a _buffer
    field of type collections.deque.
    """

    def receive(self):

        """
        If the buffer has messages, then receive from it. If the buffer
        is empty, then fill from the queue before receiving. Both
        scenarios wait as specified.
        """

        if not self._buffer:
            self._fill_buffer()
        try:
            # Remove a message from the head of the buffer.
            message = self._buffer.popleft()
        except IndexError:
            message = 'The receive operation timed out.'
            raise consuming.exceptions.ReceiveTimeout(message)
        return message

    @abc.abstractmethod
    def _fill_buffer(self):

        """
        Returns
        -------
        None
        """

        raise NotImplementedError


class ConcurrentLinkedQueue(BaseBuffering):

    def __init__(self,
                 queue,
                 batch_size_maximum_count,
                 countdown_timer,
                 _buffer=None):

        """
        Parameters
        ----------
        queue : queue.Queue
        batch_size_maximum_count : int
            Maximum size of the batch. The units are in number of
            messages.
        countdown_timer : downloadbot.common.utility.CountdownTimer
        """

        self._queue = queue
        self._batch_size_maximum_count = batch_size_maximum_count
        self._countdown_timer = countdown_timer

        self._buffer = _buffer if _buffer is not None else collections.deque()

    def _fill_buffer(self):
        # A deque should not be used instead because its maxlen
        # parameter follows circularly linked list semantics rather
        # than static array semantics.
        data = list()
        self._countdown_timer.start()

        # This must run at least once (i.e. do-while semantics).
        while True:
            # Iterative Case
            try:
                x = self._queue.get(block=False)
            except queue.Empty:
                pass
            else:
                data.append(x)

            # Base Case: maximum batch size
            if len(data) == self._batch_size_maximum_count:
                break
            # Base Case: no time remaining
            if not self._countdown_timer.has_time_remaining:
                break

        self._countdown_timer.reset()

        for x in data:
            # Should this instead create messages by using a factory?
            message = messaging.messages.Message(
                id=str(uuid.uuid4()),
                body=str(x),
                delivery_receipt=str(uuid.uuid4()))
            # Add a message to the tail of the buffer.
            self._buffer.append(message)

    def dispose(self):
        pass

    def __repr__(self):
        repr_ = ('{}('
                 'queue={}, '
                 'batch_size_maximum_count={}, '
                 'countdown_timer={})')
        return repr_.format(self.__class__.__name__,
                            self._queue,
                            self._batch_size_maximum_count,
                            self._countdown_timer)


class SqsFifoQueue(BaseBuffering):

    def __init__(self,
                 sqs_queue,
                 batch_size_maximum_count,
                 wait_time_seconds,
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
        """

        self._sqs_queue = sqs_queue
        self._batch_size_maximum_count = batch_size_maximum_count
        self._wait_time_seconds = wait_time_seconds

        self._buffer = _buffer if _buffer is not None else collections.deque()

    def _fill_buffer(self):
        messages = self._sqs_queue.receive_messages(
            MaxNumberOfMessages=self._batch_size_maximum_count,
            WaitTimeSeconds=self._wait_time_seconds)

        for message in messages:
            marshalled = messaging.messages.Message(
                id=message.message_id,
                body=message.body,
                delivery_receipt=message.receipt_handle)
            self._buffer.append(marshalled)

    def dispose(self):
        # Base Case: null or zero-valued buffer
        if not self._buffer:
            return

        Entries = [
            {
                'Id': message.id,
                'ReceiptHandle': message.delivery_receipt,
                'VisibilityTimeout': 0
            }
            for message
            in self._buffer]
        response = self._sqs_queue.change_message_visibility_batch(
            Entries=Entries)

        # What should these do instead?
        if response['ResponseMetadata']['HTTPStatusCode'] != HttpStatus.OK:
            pass
        if 'Failed' in response:
            # There can be failures even when the call returns an HTTP
            # status code of 200.
            pass

    def __repr__(self):
        repr_ = ('{}('
                 'sqs_queue={}, '
                 'batch_size_maximum_count={}, '
                 'wait_time_seconds={})')
        return repr_.format(self.__class__.__name__,
                            self._sqs_queue,
                            self._batch_size_maximum_count,
                            self._wait_time_seconds)


class Logging(Disposable):

    def __init__(self, receiver, logger):

        """
        Component to include logging.

        Parameters
        ----------
        receiver : downloadbot.infrastructure.consuming.receivers.Disposable
        logger : logging.Logger
        """

        self._receiver = receiver
        self._logger = logger

    def receive(self):
        try:
            message = self._receiver.receive()
        except consuming.exceptions.ReceiveTimeout as e:
            # An expected case has occurred. This should be handled
            # higher up in the stack.
            self._logger.debug(msg=utility.format_exception(e=e))
            raise
        else:
            msg = 'The message <{}> was received.'.format(repr(message))
            self._logger.debug(msg=msg)
            return message

    def dispose(self):
        self._receiver.dispose()

    def __repr__(self):
        repr_ = '{}(receiver={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._receiver,
                            self._logger)
