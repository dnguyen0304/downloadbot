# -*- coding: utf-8 -*-

import abc

from downloadbot.common import messaging


class Base(messaging.filters.Message):

    def filter(self, message):
        if not self._should_filter(message=message):
            self._process(message=message)
            return message

    @abc.abstractmethod
    def _should_filter(self, message):

        """
        Determine if the message should be filtered.

        Parameters
        ----------
        message : downloadbot.common.messaging.messages.Message

        Returns
        -------
        bool
            True if the message should be filtered.
        """

        raise NotImplementedError

    def _process(self, message):

        """
        Apply arbitrary mutations to the message.

        Parameters
        ----------
        message : downloadbot.common.messaging.messages.Message

        Returns
        -------
        downloadbot.common.messaging.messages.Message
        """

        return message


class DoublesMetagame(Base):

    _DOUBLES_METAGAME_NAME = 'doubles'

    """
    Reject all battles from the Doubles metagame.
    """

    def _should_filter(self, message):
        _, metagame_name, _ = message.body.split('-')
        if self._DOUBLES_METAGAME_NAME in metagame_name:
            return True
        else:
            return False

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class EveryFirstN(Base):

    def __init__(self, n):

        """
        Reject every first n messages.

        For example, if n is equal to 4, then the 5th, 10th, and so on
        messages would be accepted.

        Parameters
        ----------
        n : int
            Number of messages to reject before accepting one.
        """

        self._n = n
        self._message_count = 0

    def _should_filter(self, message):
        self._message_count += 1
        if self._message_count <= self._n:
            return True
        else:
            self._message_count = 0
            return False

    def __repr__(self):
        repr_ = '{}(n={})'
        return repr_.format(self.__class__.__name__, self._n)


class ExceptGeneration7Metagame(Base):

    _GENERATION_7_METAGAME_NAME = 'gen7'

    """
    Accept battles only from the Generation 7 metagame.
    """

    def _should_filter(self, message):
        _, metagame_name, _ = message.body.split('-')
        if metagame_name.startswith(self._GENERATION_7_METAGAME_NAME):
            return False
        else:
            return True

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class ExceptOverusedMetagame(Base):

    _OVERUSED_METAGAME_NAME = 'ou'

    """
    Accept battles only from the Overused metagame.
    """

    def _should_filter(self, message):
        _, metagame_name, _ = message.body.split('-')
        if metagame_name.endswith(self._OVERUSED_METAGAME_NAME):
            return False
        else:
            return True

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
