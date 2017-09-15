# -*- coding: utf-8 -*-

import abc


class IDownloadValidator(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self):

        """
        Returns
        -------
        str
            Path to the newest file.
        """

        pass


class IReplayDownloader(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self, url):

        """
        Parameters
        ----------
        url : str
        """

        pass

    @abc.abstractmethod
    def dispose(self):
        pass
