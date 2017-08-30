# -*- coding: utf-8 -*-

import abc


class FlushStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def should_flush(self, collection):

        """
        Parameters
        ----------
        collection : collections.Sequence

        Returns
        -------
        bool
            True if the collection should be flushed.
        """

        pass


class AfterDuration(FlushStrategy):

    def __init__(self, countdown_timer):

        """
        Parameters
        ----------
        countdown_timer : clare.common.utilities.timers.CountdownTimer
        """

        self._countdown_timer = countdown_timer

    def should_flush(self, collection):
        if not self._countdown_timer.is_running:
            self._countdown_timer.start()
            should_flush = False
        else:
            should_flush = not self._countdown_timer.has_time_remaining

        if should_flush:
            self._countdown_timer.reset()

        return should_flush

    def __repr__(self):
        repr_ = '{}(countdown_timer={})'
        return repr_.format(self.__class__.__name__, self._countdown_timer)


class AfterSize(FlushStrategy):

    def __init__(self, maximum_size):

        """
        Parameters
        ----------
        maximum_size : int
        """

        self._maximum_size = maximum_size

    def should_flush(self, collection):
        if len(collection) >= self._maximum_size:
            should_flush = True
        else:
            should_flush = False
        return should_flush

    def __repr__(self):
        repr_ = '{}(maximum_size={})'
        return repr_.format(self.__class__.__name__, self._maximum_size)
