# -*- coding: utf-8 -*-

import abc


class Receiver(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def receive(self):

        """
        Returns
        -------
        clare.common.messaging.models.Message

        Raises
        ------
        clare.common.messaging.consumer.ReceiveTimeout
            If there weren't any buffered messages and the operation
            took too long to receive the configured number of messages.
        """

        raise NotImplementedError
