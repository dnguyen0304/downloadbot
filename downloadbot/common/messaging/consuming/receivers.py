# -*- coding: utf-8 -*-

import abc


class Receiver(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def receive(self):

        """
        Receive gets a message from the queue.

        Returns
        -------
        downloadbot.common.messaging.messages.Message

        Raises
        ------
        downloadbot.common.messaging.consuming.exceptions.ReceiveTimeout
            If the operation took too long to receive the configured
            number of messages.
        """

        raise NotImplementedError
