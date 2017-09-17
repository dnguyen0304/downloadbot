# -*- coding: utf-8 -*-

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from . import exceptions


class title_not_equal(object):

    def __init__(self, title):
        self._title = title

    def __call__(self, web_driver):
        return self._title != web_driver.title


class PokemonShowdown(object):

    def __init__(self, wait_context):

        """
        This object assumes a request has already been issued to the
        web driver to start rendering the page.

        Parameters
        ----------
        wait_context : selenium.webdriver.support.ui.WebDriverWait
        """

        self._wait_context = wait_context

    def check_room_was_entered(self):

        """
        Assert the room was entered successfully.

        Returns
        -------
        None

        Raises
        ------
        roomlistwatcher.common.automation.exceptions.ValidationFailed
            If the room was not entered successfully.
        """

        condition = title_not_equal(title='Showdown!')
        try:
            self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            message = 'The room could not be entered.'
            raise exceptions.ValidationFailed(message)

    def check_connection_exists(self):

        """
        Assert the connection was established successfully.

        Returns
        -------
        None

        Raises
        ------
        roomlistwatcher.common.automation.exceptions.ConnectionLost
            If the connection was not established successfully or was lost.
        """

        css_selector = 'body > div.ps-overlay > div > form > p:first-child'
        locator = (By.CSS_SELECTOR, css_selector)
        text_ = 'disconnected'
        condition = expected_conditions.text_to_be_present_in_element(
            locator=locator,
            text_=text_)
        try:
            self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            pass
        else:
            message = 'The connection with the target server was lost.'
            raise exceptions.ConnectionLost(message)

    def __repr__(self):
        repr_ = '{}(wait_context={})'
        return repr_.format(self.__class__.__name__, self._wait_context)
