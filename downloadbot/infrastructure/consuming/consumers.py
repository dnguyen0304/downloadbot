# -*- coding: utf-8 -*-

from downloadbot.common import utility
from downloadbot.common.messaging import consuming


class Orchestrating(consuming.consumers.Consumer):

    def __init__(self, consumer, logger):

        """
        Extend to include error handling and logging.

        Parameters
        ----------
        consumer : downloadbot.common.messaging.consuming.consumers.Consumer
        logger : logging.Logger
        """

        self._consumer = consumer
        self._logger = logger

    def consume(self):
        self._logger.debug(msg='The consume operation has started.')
        try:
            self._consumer.consume()
        except Exception as e:
            message = utility.format_exception(e=e)
            self._logger.critical(msg=message, exc_info=True)
        finally:
            self._logger.debug(msg='The consume operation has completed.')

    def __repr__(self):
        repr_ = '{}(consumer={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._consumer,
                            self._logger)
