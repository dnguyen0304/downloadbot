# -*- coding: utf-8 -*-

import abc

from . import exceptions
from .common import automation


# This could be evaluated for being migrated to common.
class PageInitializer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def initialize(self, web_driver, url):

        """
        Initialize the page.

        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver
        url : str

        Returns
        -------
        None

        Raises
        ------
        downloadbot.common.automation.exceptions.AutomationFailed
            If the page was not initialized successfully.
        """

        raise NotImplementedError


class SeleniumPage(PageInitializer):

    def initialize(self, web_driver, url):
        web_driver.get(url=url)

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class PostValidating(PageInitializer):

    def __init__(self, initializer, validator):

        """
        Extend to include validation.

        Validation occurs after the page is initialized.

        Parameters
        ----------
        initializer : downloadbot.page_initializers.PageInitializer
        validator : downloadbot.common.automation.validators.PokemonShowdown
        """

        self._initializer = initializer
        self._validator = validator

    def initialize(self, web_driver, url):

        """
        Raises
        ------
        downloadbot.common.automation.exceptions.ConnectionLost
            If the connection was not established successfully or was lost.
        downloadbot.common.automation.exceptions.RoomExpired
            If the room has expired.
        """

        self._initializer.initialize(web_driver=web_driver, url=url)

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

    def __repr__(self):
        repr_ = '{}(initializer={}, validator={})'
        return repr_.format(self.__class__.__name__,
                            self._initializer,
                            self._validator)
