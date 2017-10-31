# -*- coding: utf-8 -*-

import abc
import time

from . import exceptions


class Consumer(metaclass=abc.ABCMeta):

    # Should this instead raise an exception when it fails to receive
    # or handle a message?
    @abc.abstractmethod
    def consume(self):

        """
        Receive and handle messages.

        Returns
        -------
        downloadbot.common.messaging.filters.Message
        """

        raise NotImplementedError


class Simple(Consumer):

    def __init__(self, receiver, handler, filters=None):

        """
        Parameters
        ----------
        receiver : downloadbot.common.messaging.consuming.receivers.Receiver
        handler : downloadbot.common.messaging.consuming.handlers.Handler
        filters : typing.Iterable[downloadbot.common.messaging.filters.Message]
            Defaults to list.
        """

        self._receiver = receiver
        self._handler = handler
        self._filters = filters or list()

    def consume(self):
        try:
            message = self._receiver.receive()
        except exceptions.ReceiveTimeout:
            pass
        else:
            for filter_ in self._filters:
                message = filter_.filter(message=message)
                if message is None:
                    break
            else:
                self._handler.handle(message=message)

    def __repr__(self):
        repr_ = '{}(receiver={}, handler={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._receiver,
                            self._handler,
                            self._filters)


class Blocking(Consumer):

    def __init__(self, consumer, interval, _sleeper=None):

        """
        Extend to include blocking.

        Parameters
        ----------
        consumer : downloadbot.common.messaging.consuming.consumers.Consumer
        interval : float
            Rate of work. The units are in seconds.
        """

        self._consumer = consumer
        self._interval = interval
        self._sleeper = _sleeper or time

    def consume(self):
        while True:
            self._consumer.consume()
            self._sleeper.sleep(self._interval)

    def __repr__(self):
        repr_ = '{}(consumer={}, interval={})'
        return repr_.format(self.__class__.__name__,
                            self._consumer,
                            self._interval)
