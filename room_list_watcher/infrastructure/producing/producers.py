# -*- coding: utf-8 -*-

import abc
import time

from room_list_watcher.common import io
from room_list_watcher.common import messaging
from room_list_watcher.common import retry
from room_list_watcher.common import utility


class Disposable(messaging.producing.producers.Producer, io.Disposable):

    __metaclass__ = abc.ABCMeta


class Simple(Disposable):

    def __init__(self, sender, source, filters=None):

        """
        Parameters
        ----------
        source : room_list_watcher.infrastructure.producing.sources.Disposable
        sender : room_list_watcher.common.messaging.producing.senders.Sender
        filters : typing.Iterable[room_list_watcher.common.messaging.filters.StringFilter]
            Defaults to list.
        """

        self._source = source
        self._sender = sender
        self._filters = filters or list()

    def produce(self):
        data = self._source.emit()
        for filter_ in self._filters:
            data = filter_.filter(data)
            if data is None:
                break
        else:
            self._sender.send(data=data)

    def dispose(self):
        self._source.dispose()

    def __repr__(self):
        repr_ = '{}(source={}, sender={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._source,
                            self._sender,
                            self._filters)


class Blocking(Disposable):

    def __init__(self, producer, interval, _sleeper=None):

        """
        Parameters
        ----------
        producer : room_list_watcher.infrastructure.producing.producers.Disposable
        interval : float
        """

        self._producer = producer
        self._interval = interval
        self._sleeper = _sleeper or time

    def produce(self):
        while True:
            self._producer.produce()
            self._sleeper.sleep(self._interval)

    def dispose(self):
        self._producer.dispose()

    def __repr__(self):
        repr_ = '{}(producer={}, interval={})'
        return repr_.format(self.__class__.__name__,
                            self._producer,
                            self._interval)


class Orchestrating(Disposable):

    def __init__(self, producer, logger, policy):

        """
        Extend to include error handling and logging.

        Parameters
        ----------
        producer : room_list_watcher.infrastructure.producing.producers.Disposable
        logger : logging.Logger
        policy : room_list_watcher.common.retry.policy.Policy
        """

        self._producer = producer
        self._logger = logger
        self._policy = policy

    def produce(self):
        try:
            self._policy.execute(self._producer.produce)
        except retry.exceptions.MaximumRetry as e:
            message = utility.format_exception(e=e)
            self._logger.critical(msg=message)
            self.dispose()
            raise
        except Exception as e:
            message = utility.format_exception(e=e)
            self._logger.critical(msg=message, exc_info=True)
            self.dispose()
            raise

    def dispose(self):
        self._producer.dispose()

    def __repr__(self):
        repr_ = '{}(producer={}, logger={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._producer,
                            self._logger,
                            self._policy)
