# -*- coding: utf-8 -*-

import abc

from clare.common import messaging


class BaseFilter(messaging.interfaces.IFilter):

    def filter(self, record):
        if not self._should_filter(record=record):
            self._process(record=record)
            return record

    @abc.abstractmethod
    def _should_filter(self, record):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record

        Returns
        -------
        bool
            True if the record should be filtered.
        """

        pass

    def _process(self, record):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record

        Returns
        -------
        clare.common.messaging.records.Record
        """

        return record


class DoublesBattleFilter(BaseFilter):

    def _should_filter(self, record):
        _, metagame_name, _ = record.value.split('-')
        if 'doubles' in metagame_name:
            return True
        else:
            return False

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class EveryFirstNFilter(BaseFilter):

    def __init__(self, n):

        """
        Parameters
        ----------
        n : int
            Number of records to reject before accepting one.
        """

        self._n = n
        self._record_count = 0

    def _should_filter(self, record):
        self._record_count += 1
        if self._record_count <= self._n:
            return True
        else:
            self._record_count = 0
            return False

    def __repr__(self):
        repr_ = '{}(n={})'
        return repr_.format(self.__class__.__name__, self._n)


class ExceptGenerationSevenMetagameFilter(BaseFilter):

    def _should_filter(self, record):
        _, metagame_name, _ = record.value.split('-')
        if metagame_name.startswith('gen7'):
            return False
        else:
            return True

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class ExceptOverusedMetagameFilter(BaseFilter):

    def _should_filter(self, record):
        _, metagame_name, _ = record.value.split('-')
        if metagame_name.endswith('ou'):
            return False
        else:
            return True

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
