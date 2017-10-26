# -*- coding: utf-8 -*-

from . import exceptions
from clare import common
from clare.common import messaging
from clare.common import retry


class MarshallingHandler(messaging.consumer.interfaces.IHandler):

    def __init__(self, handler, strategy):

        """
        Parameters
        ----------
        handler : clare.common.messaging.consumer.interfaces.IHandler
        strategy : clare.application.download_bot.marshall_strategies.StringToRecordMarshallStrategy
        """

        self._handler = handler
        self._strategy = strategy

    def handle(self, record):
        result = self._handler.handle(message=record)
        marshalled_result = self._strategy.marshall(result)
        return marshalled_result

    def __repr__(self):
        repr_ = '{}(handler={}, strategy={})'
        return repr_.format(self.__class__.__name__,
                            self._handler,
                            self._strategy)


class NopHandler(messaging.consumer.interfaces.IHandler):

    def handle(self, record):
        pass

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class OrchestratingHandler(messaging.consumer.interfaces.IHandler):

    def __init__(self, handler, logger):

        """
        Parameters
        ----------
        handler : clare.common.messaging.consumer.interfaces.IHandler
        logger : logging.Logger
        """

        self._handler = handler
        self._logger = logger

    def handle(self, record):
        try:
            self._handler.handle(message=record)
        except retry.exceptions.MaximumRetry as e:
            message = common.logging.utilities.format_exception(e=e)
            self._logger.debug(msg=message)

    def __repr__(self):
        repr_ = '{}(handler={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._handler,
                            self._logger)
