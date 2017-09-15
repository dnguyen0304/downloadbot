# -*- coding: utf-8 -*-

import abc


class Sender(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send(self, data):

        """
        Parameters
        ----------
        data : str

        Returns
        -------
        None

        Raises
        ------
        roomlistwatcher.common.messaging.producing.exceptions.SendTimeout
            If the sender times out.
        """

        raise NotImplementedError
