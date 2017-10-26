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
