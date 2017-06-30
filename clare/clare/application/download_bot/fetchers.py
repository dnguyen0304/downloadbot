# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import collections

from . import interfaces
from clare.common import messaging


class Fetcher(interfaces.IFetcher):

    def __init__(self, queue):

        """
        Parameters
        ----------
        queue : Queue.Queue
        """

        self._queue = queue

    def pop(self, block, timeout):
        try:
            record = self._queue.get(block=block, timeout=timeout)
        except queue.Empty:
            if not block or not timeout:
                message = 'The fetcher timed out immediately.'
            else:
                message = 'The fetcher timed out after {timeout} seconds.'.format(
                    timeout=timeout)
            raise messaging.consumer.exceptions.FetchTimeout(message)
        else:
            return record

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)


class BufferingFetcher(interfaces.IFetcher):

    def __init__(self, fetcher, size, countdown_timer):

        """
        Parameters
        ----------
        fetcher : clare.application.download_bot.interfaces.IFetcher
        size : int
        countdown_timer : clare.common.utilities.timers.CountdownTimer
        """

        self._fetcher = fetcher
        self._size = size
        self._countdown_timer = countdown_timer

        self._buffer = collections.deque()

    def pop(self, block, timeout):

        """
        If the buffer has records, then fetch from the buffer. If the
        buffer is empty, then fill from the queue before fetching. Both
        scenarios block and wait as specified.
        """

        self._countdown_timer.start()

        if not self._buffer:
            for i in xrange(self._size):
                record = self._fetcher.pop(block=block, timeout=timeout)
                self._buffer.append(record)

                if not self._countdown_timer.has_time_remaining:
                    message = 'The fetcher timed out after at least {timeout} seconds.'
                    raise messaging.consumer.exceptions.FetchTimeout(
                        message.format(timeout=timeout))

        self._countdown_timer.reset()
        record = self._buffer.popleft()
        return record

    def __repr__(self):
        repr_ = '{}(fetcher={}, size={}, countdown_timer={})'
        return repr_.format(self.__class__.__name__,
                            self._fetcher,
                            self._size,
                            self._countdown_timer)


class MeasuringFetcher(interfaces.IFetcher):

    def __init__(self, fetcher, queue_client):

        """
        Parameters
        ----------
        fetcher : clare.application.download_bot.interfaces.IFetcher
        queue_client : clare.application.download_bot.queue_clients.QueueClient
        """

        self._fetcher = fetcher
        self._queue_client = queue_client

    def pop(self, block, timeout):
        record = self._fetcher.pop(block=block, timeout=timeout)
        return record

    def calculate_message_count(self):
        message_count = self._queue_client.calculate_message_count()
        return message_count

    def __repr__(self):
        repr_ = '{}(fetcher={}, queue_client={})'
        return repr_.format(self.__class__.__name__,
                            self._fetcher,
                            self._queue_client)
