# -*- coding: utf-8 -*-

import abc


class Notifyable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify(self, event):

        """
        Parameters
        ----------
        event : str

        Returns
        ------
        None
        """

        pass


class Observable(Notifyable):

    def __init__(self):
        self._observers = set()

    def register(self, observer):

        """
        Parameters
        ----------
        observer : downloadbot.common.event.notifiables.Notifyable
        """

        self._observers.add(observer)

    def notify(self, event):

        """
        Parameters
        ----------
        event : str
        """

        for observer in self._observers:
            observer.notify(event=event)

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
