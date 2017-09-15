# -*- coding: utf-8 -*-

import abc


class Disposable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispose(self):

        """
        Garbage collect the resources.

        Returns
        -------
        None
        """

        raise NotImplementedError


class JsonSerializable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_json(self):

        """
        Convert the object to JSON.

        Returns
        -------
        str
        """

        raise NotImplementedError
