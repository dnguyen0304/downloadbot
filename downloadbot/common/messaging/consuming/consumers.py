# -*- coding: utf-8 -*-

import abc


class Consumer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def consume(self):

        """
        Receive and handle messages.

        Returns
        -------
        None
        """

        raise NotImplementedError
