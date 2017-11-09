# -*- coding: utf-8 -*-

import abc


class Repository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add(self, model):

        """
        Add the model to the repository.

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
