# -*- coding: utf-8 -*-

from . import deleters
from . import receivers


class _ConcurrentLinkedQueueReceiver(object):

    def __init__(self, queue, batch_size_maximum_count, wait_time_seconds):

        """
        Parameters
        ----------
        queue : Queue.Queue
        batch_size_maximum_count : int
        wait_time_seconds : int
        """

        self._queue = queue
        self._batch_size_maximum_count = batch_size_maximum_count
        self._wait_time_seconds = wait_time_seconds

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.consumer.receivers.Receiver]
        """

        # Create the countdown timer.
        countdown_timer = utilities.timers.CountdownTimer(
            duration=self._wait_time_seconds)

        # Create the message factory.
        message_factory = messaging.factories.Message2()

        return receivers.ConcurrentLinkedQueue(
            queue=self._queue,
            batch_size_maximum_count=self._batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=message_factory)

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)


class _NopDeleter(object):

    def create(self):
        return deleters.Nop()

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class _SqsFifoQueueReceiver(object):

    def __init__(self,
                 sqs_queue,
                 batch_size_maximum_count,
                 wait_time_seconds,
                 message_factory):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        batch_size_maximum_count : int
        wait_time_seconds : int
        message_factory : clare.common.messaging.factories.Message
        """

        self._sqs_queue = sqs_queue
        self._batch_size_maximum_count = batch_size_maximum_count
        self._wait_time_seconds = wait_time_seconds
        self._message_factory = message_factory

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.consumer.receivers.Receiver]
        """

        return receivers.SqsFifoQueue(
            sqs_queue=self._sqs_queue,
            batch_size_maximum_count=self._batch_size_maximum_count,
            wait_time_seconds=self._wait_time_seconds,
            message_factory=self._message_factory)

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


class _SqsFifoQueueDeleter(object):

    def __init__(self, sqs_queue):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        """

        self._sqs_queue = sqs_queue

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.consumer.deleters.Deleter]
        """

        return deleters.SqsFifoQueue(sqs_queue=self._sqs_queue)

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)
