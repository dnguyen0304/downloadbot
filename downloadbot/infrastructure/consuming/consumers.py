# -*- coding: utf-8 -*-

from downloadbot.common import utility
from downloadbot.common.messaging import consuming


class Orchestrating(consuming.consumers.Disposable):

    def __init__(self, consumer, logger):

        """
        Extend to include error handling and logging.

        Parameters
        ----------
        consumer : downloadbot.common.messaging.consuming.consumers.Disposable
        logger : logging.Logger
        """

        self._consumer = consumer
        self._logger = logger

    def consume(self):
        try:
            self._consumer.consume()
        except Exception as e:
            message = utility.format_exception(e=e)
            self._logger.critical(msg=message, exc_info=True)
            self.dispose()
        except KeyboardInterrupt:
            # This smells.
            # In Python 2.5, KeyboardInterrupt was changed to inherit
            # from BaseException so as not to be accidentally caught by
            # code that catches Exception.
            self.dispose()

    def dispose(self):
        self._consumer.dispose()

    def __repr__(self):
        repr_ = '{}(consumer={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._consumer,
                            self._logger)
