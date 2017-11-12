# -*- coding: utf-8 -*-

import abc


class IWaitStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def compute_wait_time(self, attempt):

        """
        Parameters
        ----------
        attempt : clare.common.retry.attempt.Attempt

        Returns
        -------
        float
            Wait time in seconds.
        """

        pass


class Fixed(IWaitStrategy):

    def __init__(self, wait_time):
        self._wait_time = wait_time

    def compute_wait_time(self, attempt):
        return self._wait_time

    def __repr__(self):
        repr_ = '{}(wait_time={})'
        return repr_.format(self.__class__.__name__, self._wait_time)
