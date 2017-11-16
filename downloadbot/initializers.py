# -*- coding: utf-8 -*-

import abc

from . import automation
from . import exceptions


# This could be evaluated for being migrated to common.
class Page(metaclass=abc.ABCMeta):

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
        downloadbot.automation.exceptions.AutomationFailed
            If the page was not initialized successfully.
        """

        raise NotImplementedError


class Selenium(Page):

    def initialize(self, web_driver, url):
        web_driver.get(url=url)

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class PostValidating(Page):

    def __init__(self, page_initializer, validator):

        """
        Extend to include validation.

        Validation occurs after the page is initialized.

        Parameters
        ----------
        page_initializer : downloadbot.initializers.Page
        validator : downloadbot.automation.validators.PokemonShowdown
        """

        self._page_initializer = page_initializer
        self._validator = validator

    def initialize(self, web_driver, url):

        """
        Raises
        ------
        downloadbot.automation.exceptions.ConnectionLost
            If the connection was not established successfully or was lost.
        downloadbot.automation.exceptions.RoomExpired
            If the room has expired.
        """

        self._page_initializer.initialize(web_driver=web_driver, url=url)

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
        repr_ = '{}(page_initializer={}, validator={})'
        return repr_.format(self.__class__.__name__,
                            self._page_initializer,
                            self._validator)
