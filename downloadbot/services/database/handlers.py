# -*- coding: utf-8 -*-

import abc


class Event(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle(self, event):

        """
        Handle the event.

        Parameters
        ----------
        event : typing.Mapping

        Returns
        -------
        typing.Mapping

        Raises
        ------
        None
        """

        raise NotImplementedError
