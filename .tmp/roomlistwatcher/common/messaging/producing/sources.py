# -*- coding: utf-8 -*-

import abc


class Source(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def emit(self):

        """
        Returns
        -------
        str

        Raises
        ------
        roomlistwatcher.common.messaging.producing.exceptions.EmitFailed
            If the source fails to emit data.
        """

        raise NotImplementedError
