# -*- coding: utf-8 -*-

import abc


class IRecord(object):

    __metaclass__ = abc.ABCMeta

    # Using the classmethod and abc.abstractmethod decorators
    # together is not supported until Python 3.3.
    @abc.abstractmethod
    def from_message(cls, message):
        pass
