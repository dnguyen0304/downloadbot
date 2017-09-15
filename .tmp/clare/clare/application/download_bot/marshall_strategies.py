# -*- coding: utf-8 -*-


class StringToRecordMarshallStrategy(object):

    def __init__(self, record_factory):

        """
        Parameters
        ----------
        record_factory : clare.common.messaging.factories.RecordFactory
        """

        self._record_factory = record_factory

    def marshall(self, value):

        """
        Parameters
        ----------
        value : str
        """

        record = self._record_factory.create(value=value)
        return record

    def __repr__(self):
        repr_ = '{}(record_factory={})'
        return repr_.format(self.__class__.__name__, self._record_factory)
