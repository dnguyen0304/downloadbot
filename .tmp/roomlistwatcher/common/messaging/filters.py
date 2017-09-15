# -*- coding: utf-8 -*-

import abc


class StringFilter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def filter(self, string):

        """
        Parameters
        ----------
        string : str

        Returns
        -------
        str
            If the data should not be filtered. Otherwise None.
        """

        raise NotImplementedError
