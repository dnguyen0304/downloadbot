# -*- coding: utf-8 -*-

import abc


class Event(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def INTERFACE_VERSION(self):
        raise NotImplementedError
