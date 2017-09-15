# -*- coding: utf-8 -*-

from roomlistwatcher.common import messaging


class NoDuplicateString(messaging.filters.StringFilter):

    def __init__(self, flush_strategy):

        """
        Processing, if applicable, is applied in-place. Flushing, if
        applicable, occurs last.

        Parameters
        ----------
        flush_strategy : roomlistwatcher.infrastructure.producing.flush_strategies.FlushStrategy
            Strategy for determining if the collection of strings should
            be flushed.
        """

        self._flush_strategy = flush_strategy

        # This object is backed by both a list and set. The space
        # complexity for these data structures is amortized. In
        # general, there is an additional memory overhead of about %25.
        # Data is duplicated between the two data structures, but this
        # avoids having to type cast the set into a
        # collections.Sequence, an O(n) operation, every time the flush
        # strategy is called.
        self._collection = list()
        self._seen = set()

    def filter(self, string):
        if not self._should_filter(string=string):
            self._process(string=string)
        else:
            string = None
        if self._flush_strategy.should_flush(collection=self._collection):
            self._collection = list()
            self._seen = set()
        return string

    def _should_filter(self, string):

        """
        Parameters
        ----------
        string : str

        Returns
        -------
        bool
            True if the string should be filtered. False otherwise.
        """

        if string in self._seen:
            should_filter = True
        else:
            self._collection.append(string)
            self._seen.add(string)
            should_filter = False
        return should_filter

    def _process(self, string):

        """
        Parameters
        ----------
        string : str

        Returns
        -------
        str
        """

        return string

    def __repr__(self):
        repr_ = '{}(flush_strategy={})'
        return repr_.format(self.__class__.__name__, self._flush_strategy)


class LoggingString(messaging.filters.StringFilter):

    def __init__(self, string_filter, logger):

        """
        Extension to include logging.

        Parameters
        ----------
        string_filter : roomlistwatcher.common.messaging.filters.StringFilter
        logger : logging.Logger
        """

        self._string_filter = string_filter
        self._logger = logger

    def filter(self, string):
        filtered = self._string_filter.filter(string=string)
        if filtered is None:
            self._logger.debug(
                msg='The data "{}" was filtered.'.format(string))
        else:
            self._logger.debug(
                msg='The data "{}" was not filtered.'.format(string))
        return filtered

    def __repr__(self):
        repr_ = '{}(string_filter={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._string_filter,
                            self._logger)
