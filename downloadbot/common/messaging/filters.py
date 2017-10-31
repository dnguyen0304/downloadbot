# -*- coding: utf-8 -*-

import abc


class Message(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def filter(self, message):

        """
        Implementations may mutate the input.

        Parameters
        ----------
        message : downloadbot.common.messaging.messages.Message

        Returns
        -------
        downloadbot.common.messaging.messages.Message
            If the input should not be filtered. Otherwise None.
        """

        raise NotImplementedError


class Logging(Message):

    def __init__(self, message_filter, logger):

        """
        Component to include logging.

        Parameters
        ----------
        message_filter : downloadbot.common.messaging.filters.Message
        logger : logging.Logger
        """

        self._message_filter = message_filter
        self._logger = logger

    def filter(self, message):
        result = self._message_filter.filter(message=message)
        if result is None:
            template = 'The data <{}> was filtered by <{}>.'
        else:
            template = 'The data <{}> was not filtered by <{}>.'
        self._logger.debug(msg=template.format(message, self._message_filter))
        return result

    def __repr__(self):
        repr_ = '{}(message_filter={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._message_filter,
                            self._logger)
