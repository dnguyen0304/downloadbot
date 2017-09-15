# -*- coding: utf-8 -*-

import abc


class IConsumer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def consume(self, interval):

        """
        Parameters
        ----------
        interval : float
            Rate of work. The units are in seconds.

        Returns
        -------
        None
        """

        raise NotImplementedError

    @abc.abstractmethod
    def _consume_once(self):

        """
        Returns
        -------
        None

        Raises
        ------
        clare.common.messaging.consumer.exceptions.FetchTimeout
            If the fetcher times out before fetching the minimum fetch size.
        """

        raise NotImplementedError


class IFetcher(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fetch(self):

        """
        Returns
        -------
        clare.common.messaging.models.Message

        Raises
        ------
        clare.common.messaging.consumer.exceptions.FetchTimeout
        """

        raise NotImplementedError


class IHandler(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, message):

        """
        Parameters
        ----------
        message : clare.common.messaging.models.Message
        """

        raise NotImplementedError
