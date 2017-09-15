# -*- coding: utf-8 -*-

import abc


class Disposable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def dispose(self):

        """
        Garbage collect the resource.

        Returns
        -------
        None
        """

        raise NotImplementedError
