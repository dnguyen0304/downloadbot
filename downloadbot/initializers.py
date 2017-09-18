# -*- coding: utf-8 -*-

import abc

from .common import io


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


class Disposable(Page, io.Disposable, metaclass=abc.ABCMeta):
    pass


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
