# -*- coding: utf-8 -*-

import abc


class Context(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add(self, model):

        """
        Queue the model to be synchronized.

        Parameters
        ----------
        model : downloadbot.services.database.models.Model

        Returns
        -------
        None

        Raises
        ------
        None
        """

        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):

        """
        Commit the current transaction.

        Returns
        -------
        None

        Raises
        ------
        None
        """

        raise NotImplementedError
