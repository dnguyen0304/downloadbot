# -*- coding: utf-8 -*-

import time

from . import exceptions
from . import interfaces


class Consumer(interfaces.IConsumer):

    def __init__(self, fetcher, handler, filters=None):

        """
        Parameters
        ----------
        fetcher : typing.Type[clare.common.messaging.consumer.interfaces.IFetcher]
        handler : typing.Type[clare.common.messaging.consumer.interfaces.IHandler]
        filters : typing.Iterable[clare.common.messaging.interfaces.IFilter]
            Defaults to list.
        """

        self._fetcher = fetcher
        self._handler = handler
        self._filters = filters or list()

    def consume(self, interval):
        while True:
            self._consume_once()
            time.sleep(interval)

    def _consume_once(self):
        try:
            message = self._fetcher.fetch()
        except exceptions.FetchTimeout:
            pass
        else:
            for filter_ in self._filters:
                message = filter_.filter(message=message)
                if message is None:
                    break
            else:
                self._handler.handle(message=message)

    def __repr__(self):
        repr_ = '{}(fetcher={}, handler={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._fetcher,
                            self._handler,
                            self._filters)
