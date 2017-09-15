# -*- coding: utf-8 -*-

import abc


class Producer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def produce(self):

        """
        Emit and send data.

        Returns
        -------
        None

        Raises
        ------
        roomlistwatcher.common.messaging.producing.exceptions.EmitFailed
            If the source fails to emit data.
        """

        raise NotImplementedError
