# -*- coding: utf-8 -*-

import abc

from .common import io


class Bot(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, url):

        """
        Execute a set of arbitrary, predefined instructions.

        Parameters
        ----------
        url : str

        Returns
        -------
        None

        Raises
        ------
        downloadbot.common.automation.exceptions.AutomationFailed
            If the automation failed.
        """

        raise NotImplementedError


class Disposable(Bot, io.Disposable, metaclass=abc.ABCMeta):
    pass
