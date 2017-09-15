# -*- coding: utf-8 -*-

import abc

from roomlistwatcher.common import io
from roomlistwatcher.common import messaging


class Disposable(messaging.producing.sources.Source, io.Disposable):

    __metaclass__ = abc.ABCMeta


class Deque(Disposable):

    def __init__(self, deque):

        """
        Parameters
        ----------
        deque : collections.deque
        """

        self._deque = deque

    def emit(self):
        try:
            data = self._deque.popleft()
        except IndexError:
            message = 'The source failed to emit data.'
            raise messaging.producing.exceptions.EmitFailed(message)
        else:
            return data

    def dispose(self):
        pass

    def __repr__(self):
        repr_ = '{}(deque={})'
        return repr_.format(self.__class__.__name__, self._deque)
