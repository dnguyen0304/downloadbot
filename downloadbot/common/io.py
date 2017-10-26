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


class JsonSerializable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_json(self):

        """
        Convert the object to its JSON representation.

        Returns
        -------
        str
        """

        raise NotImplementedError
