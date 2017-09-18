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


class Validating(Disposable):

    def __init__(self, bot, validator):

        """
        Extend to include validation.

        Parameters
        ----------
        bot : downloadbot.bots.Disposable
        validator : downloadbot.common.automation.validators.PokemonShowdown
        """

        self._bot = bot
        self._validator = validator

    def run(self, url):

        """
        Raises
        ------
        downloadbot.common.automation.exceptions.ConnectionLost
            If the connection was not established successfully or was lost.
        downloadbot.common.automation.exceptions.RoomExpired
            If the room has expired.
        """

        try:
            self._validator.check_room_was_entered()
        except automation.exceptions.ValidationFailed:
            try:
                self._validator.check_connection_exists()
            except automation.exceptions.ConnectionLost:
                raise
            else:
                message = 'The room has expired.'
                raise exceptions.RoomExpired(message)
        self._bot.run(url=url)

    def dispose(self):
        self._bot.dispose()

    def __repr__(self):
        repr_ = '{}(bot={}, validator={})'
        return repr_.format(self.__class__.__name__,
                            self._bot,
                            self._validator)
