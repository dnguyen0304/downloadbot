# -*- coding: utf-8 -*-

import abc

from selenium.webdriver.common.by import By

from . import exceptions
from .common import automation
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


class Download(Disposable):

    _LOCATOR = (By.CLASS_NAME, 'replayDownloadButton')

    def __init__(self, web_driver, initializer, finder, disposer):

        """
        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver
        initializer : downloadbot.initializers.Page
        finder : downloadbot.common.automation.finders.Button
        disposer : downloadbot.common.automation.disposers.WebDriver
        """

        self._web_driver = web_driver
        self._initializer = initializer
        self._finder = finder
        self._disposer = disposer

    def run(self, url):

        """
        Raises
        ------
        downloadbot.exceptions.BattleNotCompleted
            If the battle has not yet completed.
        """

        self._initializer.initialize(web_driver=self._web_driver)
        result = self._finder.find(locator=self._LOCATOR)
        try:
            download_button = result.or_error()
        except automation.exceptions.NoResultFound:
            message = 'The battle has not yet completed.'
            raise exceptions.BattleNotCompleted(message)
        else:
            download_button.click()

    def dispose(self):
        self._disposer.dispose(self._web_driver)

    def __repr__(self):
        repr_ = '{}(web_driver={}, initializer={}, finder={}, disposer={})'
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._initializer,
                            self._finder,
                            self._disposer)
