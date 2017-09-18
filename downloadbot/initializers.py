# -*- coding: utf-8 -*-

import abc


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
        """

        raise NotImplementedError


class Selenium(Page):

    def initialize(self, web_driver, url):
        web_driver.get(url=url)

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
