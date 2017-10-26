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
