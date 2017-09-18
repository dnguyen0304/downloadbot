# -*- coding: utf-8 -*-

import abc


# This could be evaluated for being migrated to common.
class Page(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def initialize(self, web_driver):

        """
        Initialize the page.

        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver

        Returns
        -------
        None
        """

        raise NotImplementedError


class Selenium(Page):

    def __init__(self, url):

        """
        Parameters
        ----------
        url : str
        """

        self._url = url

    def initialize(self, web_driver):
        web_driver.get(url=self._url)

    def __repr__(self):
        repr_ = '{}(url="{}")'
        return repr_.format(self.__class__.__name__, self._url)
