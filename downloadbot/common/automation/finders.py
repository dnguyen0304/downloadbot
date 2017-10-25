# -*- coding: utf-8 -*-

import abc

import selenium.common
from selenium.webdriver.support import expected_conditions

from downloadbot.common import lookup


class ButtonFinder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find(self, locator):

        """
        Look for the button specified by the predicate.

        Parameters
        ----------
        locator : tuple
            Two-element tuple. The first element is the select strategy.
            The second element is the value.

        Returns
        -------
        downloadbot.common.lookup.results.Find
        """

        raise NotImplementedError


class Selenium(ButtonFinder):

    def __init__(self, wait_context):

        """
        Parameters
        ----------
        wait_context : selenium.webdriver.support.ui.WebDriverWait
        """

        self._wait_context = wait_context

    def find(self, locator):
        condition = expected_conditions.element_to_be_clickable(
            locator=locator)
        try:
            button = self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            button = None

        result = lookup.results.Find(value=button, zero_value=None)
        return result
