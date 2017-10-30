# -*- coding: utf-8 -*-

import collections
import queue
import uuid

from downloadbot.common import messaging
from downloadbot.common.messaging import consuming


class ConcurrentLinkedQueue(consuming.receivers.Receiver):

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

    def __repr__(self):
        repr_ = ('{}('
                 'queue={}, '
                 'batch_size_maximum_count={}, '
                 'countdown_timer={}')
        return repr_.format(self.__class__.__name__,
                            self._queue,
                            self._batch_size_maximum_count,
                            self._countdown_timer)
