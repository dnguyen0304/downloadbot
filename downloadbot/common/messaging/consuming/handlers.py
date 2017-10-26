# -*- coding: utf-8 -*-

import abc


class Handler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle(self, message):

        """
        Parameters
        ----------
        downloadbot.common.messaging.messages.Message

        Returns
        -------
        None
        """

        raise NotImplementedError
