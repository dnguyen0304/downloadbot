# -*- coding: utf-8 -*-

import abc

from . import exceptions


class Consumer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def consume(self):

        """
        Receive and handle messages.

        Returns
        -------
        None
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
