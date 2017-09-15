# -*- coding: utf-8 -*-

import abc


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
