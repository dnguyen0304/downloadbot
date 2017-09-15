# -*- coding: utf-8 -*-

import Queue
import collections

from clare.common import messaging


class BufferingFetcher(messaging.consumer.interfaces.IFetcher):

    def __init__(self,
                 queue,
                 countdown_timer,
                 maximum_message_count,
                 buffer=None):

        """
        Parameters
        ----------
        queue : Queue.Queue
        countdown_timer : clare.common.utilities.timers.CountdownTimer
        maximum_message_count : int
        buffer : collections.deque
            Defaults to collections.deque.
        """

        self._queue = queue
        self._buffer = buffer if buffer is not None else collections.deque()
        self._countdown_timer = countdown_timer
        self._maximum_message_count = maximum_message_count
        self._minimum_message_count = 1

    def pop(self, timeout):

        """
        If the buffer has records, then fetch from it. If the buffer is
        empty, then fill from the queue before fetching. Both scenarios
        wait as specified.
        """

        self._countdown_timer.start()

        if not self._buffer:
            try:
                self.__fill(timeout=timeout)
            except messaging.consumer.exceptions.FetchTimeout:
                raise
            finally:
                self._countdown_timer.reset()

        record = self._buffer.popleft()
        return record

    def __fill(self, timeout):
        records = list()

        while True:
            # The following code must run at least once (i.e. do-while
            # semantics).
            try:
                record = self._queue.get(timeout=timeout)
            except Queue.Empty:
                pass
            else:
                records.append(record)

            if len(records) == self._maximum_message_count:
                break
            if not self._countdown_timer.has_time_remaining:
                break

        if len(records) < self._minimum_message_count:
            template = 'The fetcher timed out after {timeout} seconds.'
            message = template.format(timeout=timeout)
            raise messaging.consumer.exceptions.FetchTimeout(message)

        self._buffer.extend(records)

    def __repr__(self):
        repr_ = ('{}('
                 'queue={}, '
                 'buffer={}, '
                 'countdown_timer={}, '
                 'maximum_message_count={})')
        return repr_.format(self.__class__.__name__,
                            self._queue,
                            self._buffer,
                            self._countdown_timer,
                            self._maximum_message_count)
